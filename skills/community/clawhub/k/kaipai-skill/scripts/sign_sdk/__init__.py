"""Sign SDK module - backward compatibility layer.

This module re-exports from SDK for backward compatibility.
New code should import directly from sdk.auth module.
"""

import sys
from pathlib import Path

# Add SDK to path
SDK_DIR = Path(__file__).resolve().parent.parent.parent / "sdk"
if str(SDK_DIR) not in sys.path:
    sys.path.insert(0, str(SDK_DIR))

# Re-export from SDK
from sdk.auth.signer import Signer
from sdk.auth.signer import (
    BasicDateFormat,
    Algorithm,
    HeaderXDate,
    HeaderHost,
    HeaderAuthorization,
    HeaderContentSha256,
)

__all__ = [
    "Signer",
    "BasicDateFormat",
    "Algorithm",
    "HeaderXDate",
    "HeaderHost",
    "HeaderAuthorization",
    "HeaderContentSha256",
]
