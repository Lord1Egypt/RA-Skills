"""
TOTP Vault - 核心数据模型
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum


class KeyStatus(Enum):
    """密钥状态"""
    ACTIVE = "active"
    ROTATING = "rotating"
    REVOKED = "revoked"


@dataclass
class TOTPKey:
    """TOTP 密钥元数据"""
    key_id: str
    context: str
    created_at: datetime
    last_used: Optional[datetime] = None
    use_count: int = 0
    algorithm: str = "SHA1"
    digits: int = 6
    interval: int = 30
    status: KeyStatus = field(default=KeyStatus.ACTIVE)
    grace_period_until: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        return {
            "key_id": self.key_id,
            "context": self.context,
            "created_at": self.created_at.isoformat(),
            "last_used": self.last_used.isoformat() if self.last_used else None,
            "use_count": self.use_count,
            "algorithm": self.algorithm,
            "digits": self.digits,
            "interval": self.interval,
            "status": self.status.value,
            "grace_period_until": self.grace_period_until.isoformat() if self.grace_period_until else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "TOTPKey":
        return cls(
            key_id=data["key_id"],
            context=data["context"],
            created_at=datetime.fromisoformat(data["created_at"]),
            last_used=datetime.fromisoformat(data["last_used"]) if data.get("last_used") else None,
            use_count=data.get("use_count", 0),
            algorithm=data.get("algorithm", "SHA1"),
            digits=data.get("digits", 6),
            interval=data.get("interval", 30),
            status=KeyStatus(data.get("status", "active")),
            grace_period_until=datetime.fromisoformat(data["grace_period_until"]) if data.get("grace_period_until") else None
        )


@dataclass
class TOTPCode:
    """TOTP 验证码（一次性使用）"""
    code: str
    valid_from: datetime
    valid_until: datetime
    key_id: str
    
    def is_valid(self) -> bool:
        now = datetime.now()
        return self.valid_from <= now < self.valid_until


@dataclass
class MFAResult:
    """MFA 授权结果"""
    granted: bool
    key_id: str
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    
    def __bool__(self):
        return self.granted


@dataclass
class VaultBackup:
    """Vault 备份数据结构"""
    version: str
    created_at: str
    keys: list
    
    def to_dict(self) -> dict:
        return {
            "version": self.version,
            "created_at": self.created_at,
            "keys": self.keys
        }


@dataclass  
class BackupKeyEntry:
    """单个密钥的备份项"""
    key_id: str
    context: str
    encrypted_secret: str
    algorithm: str
    digits: int
    interval: int
    created_at: str
    
    def to_dict(self) -> dict:
        return {
            "key_id": self.key_id,
            "context": self.context,
            "encrypted_secret": self.encrypted_secret,
            "algorithm": self.algorithm,
            "digits": self.digits,
            "interval": self.interval,
            "created_at": self.created_at
        }