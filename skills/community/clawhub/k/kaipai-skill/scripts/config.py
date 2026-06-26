"""Script-level configuration for Kaipai AI skill.

This module imports base configuration from SDK and adds script-specific settings.
"""
import os
import sys
from pathlib import Path

# Add SDK to path if needed
SDK_DIR = Path(__file__).resolve().parent.parent / "sdk"
if str(SDK_DIR) not in sys.path:
    sys.path.insert(0, str(SDK_DIR))

# Import base configuration from SDK
from sdk.core.config import (
    WAPI_ENDPOINT,
    GID_CACHE_FILE,
    VERSION,
    USER_AGENT,
    URL_DOWNLOAD_MAX_BYTES_DEFAULT,
    URL_DOWNLOAD_CONNECT_TIMEOUT_DEFAULT,
    URL_DOWNLOAD_READ_TIMEOUT_DEFAULT,
    url_download_max_bytes,
    url_download_connect_timeout,
    url_download_read_timeout,
    url_download_timeout_tuple,
)

# Script-specific configuration
SCRIPTS_DIR = Path(__file__).parent

# Region map (overwritten by server config when fetched)
REGIONS = {}

# Invoke presets (overwritten by server config when fetched)
INVOKE = {}
