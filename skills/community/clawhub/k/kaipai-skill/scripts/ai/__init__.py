"""AI module - backward compatibility layer.

This module re-exports from SDK for backward compatibility.
New code should import directly from sdk module.
"""

import sys
from pathlib import Path

# Add SDK to path
SDK_DIR = Path(__file__).resolve().parent.parent.parent / "sdk"
if str(SDK_DIR) not in sys.path:
    sys.path.insert(0, str(SDK_DIR))

# Re-export from SDK
from sdk.core.api import AiApi
from sdk.core.config import (
    WAPI_ENDPOINT,
    VERSION,
    USER_AGENT,
    url_download_max_bytes,
    url_download_timeout_tuple,
)
from sdk.utils.cache import GidCache

__all__ = [
    "AiApi",
    "WAPI_ENDPOINT",
    "VERSION",
    "USER_AGENT",
    "url_download_max_bytes",
    "url_download_timeout_tuple",
    "GidCache",
]
