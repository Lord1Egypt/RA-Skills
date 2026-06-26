"""
HTTP 授权服务 - 数据模型
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any


class AuthStatus(Enum):
    """授权请求状态"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    DENIED = "denied"
    EXPIRED = "expired"


class Decision(Enum):
    """授权决策"""
    GRANT = "grant"
    DENY = "deny"
    PENDING = "pending"


@dataclass
class PendingAuthRequest:
    """待处理的授权请求"""
    request_id: str
    agent_id: str
    resource_path: str
    operation: str
    data_level: str
    context: Dict[str, Any]
    status: AuthStatus
    created_at: datetime
    expires_at: datetime
    confirmed_at: Optional[datetime] = None
    decision: Optional[Decision] = None
    auth_token_hash: Optional[str] = None
    confirmed_by: Optional[str] = None


@dataclass
class AuthRequest:
    """授权请求（来自内控 Skill）"""
    agent_id: str
    resource_path: str
    operation: str  # READ / WRITE / DELETE / EXECUTE
    data_level: str
    context: Dict[str, Any] = field(default_factory=dict)
    timeout_seconds: int = 120


@dataclass
class AuthResponse:
    """授权响应"""
    decision: Decision
    method: Optional[str] = None
    message: str = ""
    request_id: Optional[str] = None


@dataclass
class AuthRequestResponse:
    """创建授权请求的响应"""
    request_id: str
    status: str
    confirmation_url: str
    expires_at: datetime


@dataclass
class AuthStatusResponse:
    """授权状态查询响应"""
    request_id: str
    status: str
    created_at: datetime
    expires_at: datetime
    confirmed_at: Optional[datetime] = None
    decision: Optional[str] = None


@dataclass
class ConfirmRequest:
    """用户确认请求"""
    user_identifier: Optional[str] = None


@dataclass
class ConfirmResponse:
    """确认响应"""
    success: bool
    message: str
