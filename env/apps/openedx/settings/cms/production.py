# -*- coding: utf-8 -*-
import os
from cms.envs.production import *

####### Settings common to LMS and CMS
import json
import os

from xmodule.modulestore.modulestore_settings import update_module_store_settings

# Mongodb connection parameters: simply modify `mongodb_parameters` to affect all connections to MongoDb.
mongodb_parameters = {
    "db": "openedx",
    "host": "mongodb",
    "port": 27017,
    "user": None,
    "password": None,
    # Connection/Authentication
    "connect": False,
    "ssl": False,
    "authsource": "admin",
    "replicaSet": None,
    
}
DOC_STORE_CONFIG = mongodb_parameters
CONTENTSTORE = {
    "ENGINE": "xmodule.contentstore.mongo.MongoContentStore",
    "ADDITIONAL_OPTIONS": {},
    "DOC_STORE_CONFIG": DOC_STORE_CONFIG
}
# Load module store settings from config files
update_module_store_settings(MODULESTORE, doc_store_settings=DOC_STORE_CONFIG)
DATA_DIR = "/openedx/data/modulestore"

for store in MODULESTORE["default"]["OPTIONS"]["stores"]:
   store["OPTIONS"]["fs_root"] = DATA_DIR

# Behave like memcache when it comes to connection errors
DJANGO_REDIS_IGNORE_EXCEPTIONS = True

# Meilisearch connection parameters
MEILISEARCH_ENABLED = True
MEILISEARCH_URL = "http://meilisearch:7700"
MEILISEARCH_PUBLIC_URL = "http://meilisearch.local.openedx.io"
MEILISEARCH_INDEX_PREFIX = "tutor_"
MEILISEARCH_API_KEY = "d6efd1fcd7bdef9db50f82007acc33071f5e7240d144e252ec31e3653e3fea25"
MEILISEARCH_MASTER_KEY = "eB7AXqjekkYiO2WgqxUNAnBC"
SEARCH_ENGINE = "search.meilisearch.MeilisearchEngine"

# Common cache config
CACHES = {
    "default": {
        "KEY_PREFIX": "default",
        "VERSION": "1",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "general": {
        "KEY_PREFIX": "general",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "mongo_metadata_inheritance": {
        "KEY_PREFIX": "mongo_metadata_inheritance",
        "TIMEOUT": 300,
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "configuration": {
        "KEY_PREFIX": "configuration",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "celery": {
        "KEY_PREFIX": "celery",
        "TIMEOUT": 7200,
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "course_structure_cache": {
        "KEY_PREFIX": "course_structure",
        "TIMEOUT": 604800, # 1 week
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "ora2-storage": {
        "KEY_PREFIX": "ora2-storage",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    }
}

# The default Django contrib site is the one associated to the LMS domain name. 1 is
# usually "example.com", so it's the next available integer.
SITE_ID = 2

# Contact addresses
CONTACT_MAILING_ADDRESS = "My Open edX - http://local.openedx.io"
DEFAULT_FROM_EMAIL = ENV_TOKENS.get("DEFAULT_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
DEFAULT_FEEDBACK_EMAIL = ENV_TOKENS.get("DEFAULT_FEEDBACK_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
SERVER_EMAIL = ENV_TOKENS.get("SERVER_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
TECH_SUPPORT_EMAIL = ENV_TOKENS.get("TECH_SUPPORT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
CONTACT_EMAIL = ENV_TOKENS.get("CONTACT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
BUGS_EMAIL = ENV_TOKENS.get("BUGS_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
UNIVERSITY_EMAIL = ENV_TOKENS.get("UNIVERSITY_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
PRESS_EMAIL = ENV_TOKENS.get("PRESS_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
PAYMENT_SUPPORT_EMAIL = ENV_TOKENS.get("PAYMENT_SUPPORT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
BULK_EMAIL_DEFAULT_FROM_EMAIL = ENV_TOKENS.get("BULK_EMAIL_DEFAULT_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
API_ACCESS_MANAGER_EMAIL = ENV_TOKENS.get("API_ACCESS_MANAGER_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
API_ACCESS_FROM_EMAIL = ENV_TOKENS.get("API_ACCESS_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])

# Get rid completely of coursewarehistoryextended, as we do not use the CSMH database
INSTALLED_APPS.remove("lms.djangoapps.coursewarehistoryextended")
DATABASE_ROUTERS.remove(
    "openedx.core.lib.django_courseware_routers.StudentModuleHistoryExtendedRouter"
)

# Set uploaded media file path
MEDIA_ROOT = "/openedx/media/"

# Video settings
VIDEO_IMAGE_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT
VIDEO_TRANSCRIPTS_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT

GRADES_DOWNLOAD = {
    "STORAGE_TYPE": "",
    "STORAGE_KWARGS": {
        "base_url": "/media/grades/",
        "location": "/openedx/media/grades",
    },
}

# ORA2
ORA2_FILEUPLOAD_BACKEND = "filesystem"
ORA2_FILEUPLOAD_ROOT = "/openedx/data/ora2"
FILE_UPLOAD_STORAGE_BUCKET_NAME = "openedxuploads"
ORA2_FILEUPLOAD_CACHE_NAME = "ora2-storage"

# Change syslog-based loggers which don't work inside docker containers
LOGGING["handlers"]["local"] = {
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "all.log"),
    "formatter": "standard",
}
LOGGING["handlers"]["tracking"] = {
    "level": "DEBUG",
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "tracking.log"),
    "formatter": "standard",
}
LOGGING["loggers"]["tracking"]["handlers"] = ["console", "local", "tracking"]

# Silence some loggers (note: we must attempt to get rid of these when upgrading from one release to the next)
LOGGING["loggers"]["blockstore.apps.bundles.storage"] = {"handlers": ["console"], "level": "WARNING"}

# These warnings are visible in simple commands and init tasks
import warnings

# REMOVE-AFTER-V20: check if we can remove these lines after upgrade.
from django.utils.deprecation import RemovedInDjango50Warning, RemovedInDjango51Warning
# RemovedInDjango5xWarning: 'xxx' is deprecated. Use 'yyy' in 'zzz' instead.
warnings.filterwarnings("ignore", category=RemovedInDjango50Warning)
warnings.filterwarnings("ignore", category=RemovedInDjango51Warning)
# DeprecationWarning: 'imghdr' is deprecated and slated for removal in Python 3.13
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pgpy.constants")

# Email
EMAIL_USE_SSL = False
# Forward all emails from edX's Automated Communication Engine (ACE) to django.
ACE_ENABLED_CHANNELS = ["django_email"]
ACE_CHANNEL_DEFAULT_EMAIL = "django_email"
ACE_CHANNEL_TRANSACTIONAL_EMAIL = "django_email"
EMAIL_FILE_PATH = "/tmp/openedx/emails"

# Language/locales
LANGUAGE_COOKIE_NAME = "openedx-language-preference"

# Allow the platform to include itself in an iframe
X_FRAME_OPTIONS = "SAMEORIGIN"


JWT_AUTH["JWT_ISSUER"] = "http://local.openedx.io/oauth2"
JWT_AUTH["JWT_AUDIENCE"] = "openedx"
JWT_AUTH["JWT_SECRET_KEY"] = "nhrRudWJnYewDCWmemwTRnF7"
JWT_AUTH["JWT_PRIVATE_SIGNING_JWK"] = json.dumps(
    {
        "kid": "openedx",
        "kty": "RSA",
        "e": "AQAB",
        "d": "As_oM6baCGyrfMtxtzai75B1gZ6dAO0h-AowhJwqNscVaL9eUy2MoBnlfb-MgkQjsDcoOphFK74ppJYaqQhhvWYXU9JMgBPjHcIPUlgqkdgU1o64ypYkGQHR3VtxNGtvemuR5VAvtuT6on-bdSnu1Y3CvE1pnkVYDcEdnjJv11Nn3L-vC7e3wX3MfEGhamgHbVyVcG7TvsFTSHX3lXP659reNG0Aiy60gk723FWLZXOa5zo58bLnjM1p-TLAdonz30XgEb2rtYvsQAspPvZaWUrOu7aKrfF16pi1BKqYdnGqOF2hgAuATruBMrfIDGLpBq22Bbl1JBlQRRI7wk_3sQ",
        "n": "rvCSqhzXHyc5GKXZhdtX5KMR4SsKdWbihHkmOUVVZn8iV-lrLI9SadTj2OMGJsthKh90dT8-k1a5Gso8TBGvByCd7a8oyz3j-AYYJ7o8_tJcQIfr5-02WKy901zXQ5aDbXukXFwaga_wUjFReIBNopb5Fv_b9Yq1yZv5g9cvcuI8Ft-g6rsDVkVCdpR6avFYqloPZGpTaqudefPgd8dQVZEiWb0Lo_fOlIWXKM0NIun_6DooMfBVY1l9tPzRDGDoN3zEWkvpUEHBmhzJCD68wMWgUisUMNK5J2-ak8fJBas6okYi3JVBd0xbGFB4vxsItbl-yF36-GnPkx9kXL1B9Q",
        "p": "xSlqeEk3HGtPt5PPIZWjMeerqXIRdtwj0oc6rrLK7zXBaqdnZ07fbVxkQbPuB4NrkVzHOWWrhJIkkAPNKp92ioYySUNInXy_CvD5kyh7_Q2LDf8lDSy603cqp2CuZWc10aH3z7PDmyp8yqF0wZovLg8FIAHRYtC3EacZx6dmph0",
        "q": "4yV1NWmPsaZrhkFkGvsa60CNZhBqEj1Z-mKQXBIfZ9jJ_hhYFE9yHx6-RTl7F9lT0hf-IT0OsBVgetj7uwKAj7IU0PZFZ3mwsJgHEtol0SkqxTpK0oghKlJxBsq0BuexJe0GEKgHY2scIEQTimQ7lEf_prgYeSiuZlk_2g36Y7k",
        "dq": "QABz8CLYTDQaI_AU5s1OHm9H6DRDzvPegIB5MJgipT4eXCw71S01eLNO5W520pd32MDN6Eut8ct0LekptN3Vn6eL2f0qPSe6s2eCxrsU4MR6uqvcHUoiHiywkDtZUoDCF2-bv-G4gzjQ6f6EiwAHEZbf3_gLXUgrK8eGCEjb_nE",
        "dp": "WIc_MmGVqGIa-lAZOnhJPdhLgRsh8l_oidiEpfrMGlrlzTD7wixtMFrC_amAIMmG3E9veTtIp49DcZLzZccSYCLfo3vduDFSSuRm_Ae6nKafIJrHFUJXZSpl8Z_8zrVoOgfjENUj6KFMRWP33BKSSrkd0QBf92HGQdvpPHfTJJU",
        "qi": "QB9he0A4f5jQm6145rPGS8X-fbhOWCAW0RZVqd_O6_0A-5fwWxDJqjHWAGGcXNfHd8G24JNxKCmebqgfvmPm_Nxe3xOk3yHQxk8UpofNbOrEt7UupxUlRoFSo6ro4UL_1zx5kkz_dtRmowhEq7g3d-olXuiIzfVXQTu-rENBzYg",
    }
)
JWT_AUTH["JWT_PUBLIC_SIGNING_JWK_SET"] = json.dumps(
    {
        "keys": [
            {
                "kid": "openedx",
                "kty": "RSA",
                "e": "AQAB",
                "n": "rvCSqhzXHyc5GKXZhdtX5KMR4SsKdWbihHkmOUVVZn8iV-lrLI9SadTj2OMGJsthKh90dT8-k1a5Gso8TBGvByCd7a8oyz3j-AYYJ7o8_tJcQIfr5-02WKy901zXQ5aDbXukXFwaga_wUjFReIBNopb5Fv_b9Yq1yZv5g9cvcuI8Ft-g6rsDVkVCdpR6avFYqloPZGpTaqudefPgd8dQVZEiWb0Lo_fOlIWXKM0NIun_6DooMfBVY1l9tPzRDGDoN3zEWkvpUEHBmhzJCD68wMWgUisUMNK5J2-ak8fJBas6okYi3JVBd0xbGFB4vxsItbl-yF36-GnPkx9kXL1B9Q",
            }
        ]
    }
)
JWT_AUTH["JWT_ISSUERS"] = [
    {
        "ISSUER": "http://local.openedx.io/oauth2",
        "AUDIENCE": "openedx",
        "SECRET_KEY": "nhrRudWJnYewDCWmemwTRnF7"
    }
]

# Enable/Disable some features globally
FEATURES["ENABLE_DISCUSSION_SERVICE"] = False
FEATURES["PREVENT_CONCURRENT_LOGINS"] = False
FEATURES["ENABLE_CORS_HEADERS"] = True

# CORS
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_INSECURE = True
# Note: CORS_ALLOW_HEADERS is intentionally not defined here, because it should
# be consistent across deployments, and is therefore set in edx-platform.

# Add your MFE and third-party app domains here
CORS_ORIGIN_WHITELIST = []

# Disable codejail support
# explicitely configuring python is necessary to prevent unsafe calls
import codejail.jail_code
codejail.jail_code.configure("python", "nonexistingpythonbinary", user=None)
# another configuration entry is required to override prod/dev settings
CODE_JAIL = {
    "python_bin": "nonexistingpythonbinary",
    "user": None,
}

OPENEDX_LEARNING = {
    'MEDIA': {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {
            "location": "/openedx/media-private/openedx-learning",
        }
    }
}


######## End of settings common to LMS and CMS

######## Common CMS settings
STUDIO_NAME = "My Open edX - Studio"

CACHES["staticfiles"] = {
    "KEY_PREFIX": "staticfiles_cms",
    "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    "LOCATION": "staticfiles_cms",
}

# Authentication
SOCIAL_AUTH_EDX_OAUTH2_SECRET = "LUmuYj7KGRCPGkHVh7nDLcvj"
SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT = "http://lms:8000"
SOCIAL_AUTH_REDIRECT_IS_HTTPS = False  # scheme is correctly included in redirect_uri
SESSION_COOKIE_NAME = "studio_session_id"

MAX_ASSET_UPLOAD_FILE_SIZE_IN_MB = 100

FRONTEND_LOGIN_URL = LMS_ROOT_URL + '/login'
FRONTEND_REGISTER_URL = LMS_ROOT_URL + '/register'

# Enable "reindex" button
FEATURES["ENABLE_COURSEWARE_INDEX"] = True

# Create folders if necessary
for folder in [LOG_DIR, MEDIA_ROOT, STATIC_ROOT, ORA2_FILEUPLOAD_ROOT]:
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)



######## End of common CMS settings

ALLOWED_HOSTS = [
    ENV_TOKENS.get("CMS_BASE"),
    "cms",
]
CORS_ORIGIN_WHITELIST.append("http://studio.local.openedx.io")

# Authentication
SOCIAL_AUTH_EDX_OAUTH2_KEY = "cms-sso"
SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT = "http://local.openedx.io"

# MFE-specific settings

COURSE_AUTHORING_MICROFRONTEND_URL = "http://apps.local.openedx.io/authoring"


LOGIN_REDIRECT_WHITELIST.append("apps.local.openedx.io")
CORS_ORIGIN_WHITELIST.append("http://apps.local.openedx.io")
CSRF_TRUSTED_ORIGINS.append("http://apps.local.openedx.io")