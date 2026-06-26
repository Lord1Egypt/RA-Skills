"""
HTTP 授权服务

提供本地 HTTP 授权通道，支持：
- Web UI 授权页面
- 系统通知
- 一次性授权令牌
"""

from .models import (
    AuthStatus,
    Decision,
    PendingAuthRequest,
    AuthRequest,
    AuthResponse,
    AuthRequestResponse,
    AuthStatusResponse,
    ConfirmRequest,
    ConfirmResponse
)
from .request_store import RequestStore
from .notifications import (
    NotificationChannel,
    WebUINotification,
    SystemNotification,
    ConsoleNotification,
    NotificationService
)
from .token_vault import SecureTokenVault
from .server import HTTPAuthService
from .integration import HTTPAuthorizationStrategy, PolicyEngineWithHTTPAuth

__all__ = [
    'AuthStatus',
    'Decision',
    'PendingAuthRequest',
    'AuthRequest',
    'AuthResponse',
    'AuthRequestResponse',
    'AuthStatusResponse',
    'ConfirmRequest',
    'ConfirmResponse',
    'RequestStore',
    'NotificationChannel',
    'WebUINotification',
    'SystemNotification',
    'ConsoleNotification',
    'NotificationService',
    'SecureTokenVault',
    'HTTPAuthService',
    'HTTPAuthorizationStrategy',
    'PolicyEngineWithHTTPAuth',
]
