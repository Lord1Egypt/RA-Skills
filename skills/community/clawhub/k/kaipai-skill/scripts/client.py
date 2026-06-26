"""Client module - backward compatibility layer.

This module re-exports from SDK for backward compatibility.
New code should import directly from sdk module.
"""

import sys
from pathlib import Path

# Add SDK to path
SDK_DIR = Path(__file__).resolve().parent.parent / "sdk"
if str(SDK_DIR) not in sys.path:
    sys.path.insert(0, str(SDK_DIR))

# Re-export from SDK
from sdk.core.client import WapiApiError, ConsumeDeniedError, WapiClient, SkillClient
from sdk.core.api import safe_url_preview

__all__ = [
    "WapiApiError",
    "ConsumeDeniedError",
    "WapiClient",
    "SkillClient",
    "safe_url_preview",
]
