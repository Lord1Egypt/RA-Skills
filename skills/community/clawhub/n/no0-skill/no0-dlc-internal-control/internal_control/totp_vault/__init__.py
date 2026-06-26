"""
TOTP Vault 模块

提供 TOTP 密钥管理和自动化 MFA 授权能力
"""

from .core import TOTPVault
from .models import TOTPKey, TOTPCode, MFAResult, KeyStatus, VaultBackup
from .storage import VaultStorage, SQLiteStorage
from .crypto import MasterKeyManager, EncryptionHelper
from .integration import (
    MFAuthorizationProvider,
    ReferenceMonitorWithMFA,
    create_simple_console_callback
)

__all__ = [
    'TOTPVault',
    'TOTPKey',
    'TOTPCode',
    'MFAResult',
    'KeyStatus',
    'VaultBackup',
    'VaultStorage',
    'SQLiteStorage',
    'MasterKeyManager',
    'EncryptionHelper',
    'MFAuthorizationProvider',
    'ReferenceMonitorWithMFA',
    'create_simple_console_callback',
]
