"""
动态分级授权联动引擎

职责：
1. 根据动态分级结果选择授权策略
2. L3 → HTTP 授权
3. L4+ → HTTP 授权 + TOTP MFA
4. 批量升级场景触发渐进式授权
5. 支持授权缓存避免重复验证
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List, Callable
from enum import Enum
from dataclasses import dataclass, field

from ..reference_monitor import (
    AccessDecision, AccessResult, DataLevel, AccessOperation
)
from .dynamic_models import DynamicClassificationResult

# 导入 HTTP 授权服务
from ..http_auth import HTTPAuthService, AuthRequest, AuthStatus

# 导入 TOTP Vault
from ..totp_vault import TOTPVault, MFAResult
from ..totp_vault.integration import MFAuthorizationProvider


logger = logging.getLogger(__name__)


def _get_level_strictness(level_value: str) -> int:
    """获取级别的严格度数值"""
    mapping = {
        'L1-PUBLIC': 1,
        'L2-INTERNAL': 2,
        'L3-RESTRICTED': 3,
        'L4-CONFIDENTIAL': 4,
        'L5-SECRET': 5,
        'L6-CRITICAL': 6,
    }
    return mapping.get(level_value, 0)


class AuthorizationStrategy(Enum):
    """授权策略枚举"""
    NONE = "none"                    # 无需授权
    HTTP_ONLY = "http_only"          # 仅 HTTP 授权
    TOTP_ONLY = "totp_only"          # 仅 TOTP MFA
    HTTP_THEN_TOTP = "http_then_totp"  # HTTP + TOTP 两步授权
    DENY = "deny"                    # 直接拒绝
