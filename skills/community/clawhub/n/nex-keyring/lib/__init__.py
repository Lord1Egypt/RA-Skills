"""
Nex Keyring - Library Package
Local API Key & Secret Rotation Tracker
"""

from .config import (
    DATA_DIR,
    DB_PATH,
    EXPORT_DIR,
    DEFAULT_ROTATION_DAYS,
    STRICT_ROTATION_DAYS,
    SERVICE_CATEGORIES,
    RISK_LEVELS,
    SERVICE_PRESETS,
    ENCRYPTION_AVAILABLE,
    ENCRYPTION_METHOD,
)
from .storage import Storage
from .scanner import (
    scan_env_file,
    scan_env_vars,
    detect_service,
    check_key_rotation,
    bulk_check,
    hash_key,
)

__version__ = "1.0.0"
__author__ = "Nex AI (Kevin Blancaflor)"
__license__ = "MIT-0"

__all__ = [
    "DATA_DIR",
    "DB_PATH",
    "EXPORT_DIR",
    "DEFAULT_ROTATION_DAYS",
    "STRICT_ROTATION_DAYS",
    "SERVICE_CATEGORIES",
    "RISK_LEVELS",
    "SERVICE_PRESETS",
    "ENCRYPTION_AVAILABLE",
    "ENCRYPTION_METHOD",
    "Storage",
    "scan_env_file",
    "scan_env_vars",
    "detect_service",
    "check_key_rotation",
    "bulk_check",
    "hash_key",
]
