"""
TOTP Vault 与 Reference Monitor 集成

职责：
1. 将 TOTP Vault 作为 MFA 授权后端接入 Reference Monitor
2. 实现自动化 MFA 流程（人类确认 + 自动 TOTP 验证）
3. 管理不同数据级别对应的 MFA 密钥上下文
"""

from datetime import datetime
from typing import Optional, Callable
from ..reference_monitor import (
    ReferenceMonitor,
    AccessDecision,
    AccessResult,
    AccessRequest,
    DataLevel,
    PolicyDecision
)
from .core import TOTPVault
from .models import MFAResult


class MFAuthorizationProvider:
    """
    MFA 授权提供者
    
    将 TOTP Vault 集成到 Reference Monitor 的授权流程中
    """
    
    # 数据级别到 TOTP 上下文的映射
    LEVEL_CONTEXT_MAP = {
        DataLevel.L3_RESTRICTED: "l3_restricted_access",
        DataLevel.L4_CONFIDENTIAL: "l4_confidential_access",
        DataLevel.L5_SECRET: "l5_secret_access",
        DataLevel.L6_CRITICAL: "l6_critical_access",
    }
    
    def __init__(self, vault: Optional[TOTPVault] = None):
        self.vault = vault or TOTPVault()
        self._confirmation_callback: Optional[Callable[[dict], bool]] = None
    
    def set_confirmation_callback(self, callback: Callable[[dict], bool]) -> None:
        """
        设置人类确认回调
        
        Args:
            callback: 接收请求信息字典，返回 bool 表示是否批准
                请求信息包含: context, key_id, expires_at
        """
        self._confirmation_callback = callback
    
    def get_context_for_level(self, level: DataLevel) -> Optional[str]:
        """获取数据级别对应的 TOTP 上下文"""
        return self.LEVEL_CONTEXT_MAP.get(level)
    
    async def request_authorization(
        self,
        request: AccessRequest,
        level: DataLevel
    ) -> AccessResult:
        """
        请求 MFA 授权
        
        流程：
        1. 确定数据级别对应的 TOTP 上下文
        2. 获取或创建 TOTP 密钥
        3. 执行 MFA 流程（预计算 TOTP -> 人类确认 -> 自动验证）
        4. 返回授权结果
        """
        # 检查是否有确认回调
        if not self._confirmation_callback:
            return AccessResult(
                decision=AccessDecision.DENY,
                token=None,
                expires_at=None,
                level=level,
                policy="mfa_not_configured",
                reason="MFA confirmation callback not configured",
                audit_record_id=""
            )
        
        # 获取上下文
        context = self.get_context_for_level(level)
        if not context:
            # 该级别不需要 MFA
            return AccessResult(
                decision=AccessDecision.ALLOW,
                token=None,
                expires_at=None,
                level=level,
                policy="no_mfa_required",
                reason="Data level does not require MFA",
                audit_record_id=""
            )
        
        # 获取或创建密钥
        from .models import KeyStatus
        key_meta = self.vault.get_key_by_context(context)
        
        if not key_meta:
            # 首次使用，生成密钥
            key_meta = self.vault.generate_key(context=context)
        elif key_meta.status == KeyStatus.ROTATING:
            # 密钥轮换中，检查是否在宽限期
            if key_meta.grace_period_until and datetime.now() < key_meta.grace_period_until:
                # 宽限期内，可以继续使用
                pass
            else:
                # 宽限期已过，需要重新生成
                key_meta = self.vault.generate_key(context=context)
        elif key_meta.status == KeyStatus.REVOKED:
            return AccessResult(
                decision=AccessDecision.DENY,
                token=None,
                expires_at=None,
                level=level,
                policy="key_revoked",
                reason="TOTP key has been revoked",
                audit_record_id=""
            )
        
        # 执行 MFA 流程
        result = self.vault.execute_mfa_flow(
            key_id=key_meta.key_id,
            human_confirmation_callback=self._confirmation_callback
        )
        
        # 构建 AccessResult
        if result.granted:
            # 生成授权令牌
            import secrets
            token = secrets.token_urlsafe(32)
            
            from datetime import timedelta
            return AccessResult(
                decision=AccessDecision.ALLOW,
                token=token,
                expires_at=datetime.now() + timedelta(minutes=5),
                level=level,
                policy="mfa_authorized",
                reason=f"MFA authorization successful via {key_meta.key_id}",
                audit_record_id=""
            )
        else:
            return AccessResult(
                decision=AccessDecision.DENY,
                token=None,
                expires_at=None,
                level=level,
                policy="mfa_denied",
                reason=result.message,
                audit_record_id=""
            )


class ReferenceMonitorWithMFA:
    """
    集成 MFA 的 Reference Monitor
    
    扩展 Reference Monitor，添加 TOTP Vault 支持的 MFA 授权能力
    """
    
    def __init__(self):
        self.monitor = ReferenceMonitor()
        self.mfa_provider = MFAuthorizationProvider()
    
    async def initialize(self):
        """初始化 Monitor 和 MFA 提供器"""
        await self.monitor.initialize()
    
    def set_mfa_confirmation_callback(self, callback: Callable[[dict], bool]) -> None:
        """设置 MFA 确认回调"""
        self.mfa_provider.set_confirmation_callback(callback)
    
    async def check_access(
        self,
        agent_id: str,
        file_path: str,
        operation: str,
        context: dict
    ) -> AccessResult:
        """
        访问控制检查（支持 MFA）
        
        流程：
        1. 调用 Reference Monitor 进行基础检查
        2. 如果需要授权（PENDING），触发 MFA 流程
        3. 返回最终结果
        """
        from ..reference_monitor import AccessOperation
        
        # 转换操作类型
        op_map = {
            'read': AccessOperation.READ,
            'write': AccessOperation.WRITE,
            'delete': AccessOperation.DELETE,
            'execute': AccessOperation.EXECUTE,
        }
        op = op_map.get(operation.lower(), AccessOperation.READ)
        
        # 基础访问检查
        result = await self.monitor.check_access(
            agent_id=agent_id,
            file_path=file_path,
            operation=op,
            context=context
        )
        
        # 如果需要授权，触发 MFA
        if result.decision == AccessDecision.PENDING:
            # 构建 AccessRequest
            request = AccessRequest(
                agent_id=agent_id,
                file_path=file_path,
                operation=op,
                context=context,
                timestamp=datetime.now()
            )
            
            # 执行 MFA 授权
            mfa_result = await self.mfa_provider.request_authorization(
                request=request,
                level=result.level
            )
            
            return mfa_result
        
        return result


# ========== 便捷函数 ==========

def create_simple_console_callback() -> Callable[[dict], bool]:
    """
    创建简单的控制台确认回调（用于演示）
    
    实际生产环境应该使用：
    - 系统通知 + Web UI
    - 飞书/钉钉/Slack 消息
    - 专用授权 App
    """
    def callback(request_info: dict) -> bool:
        print("\n" + "="*60)
        print("🔐 MFA 授权请求")
        print("="*60)
        print(f"上下文: {request_info['context']}")
        print(f"密钥ID: {request_info['key_id']}")
        print(f"过期时间: {request_info['expires_at']}")
        print("-"*60)
        print("系统已自动计算 TOTP 码（您无需输入）")
        print("请确认是否授权本次访问")
        print("-"*60)
        
        # 模拟用户输入（实际应该等待用户交互）
        # 在演示中自动确认
        import os
        if os.environ.get('TOTP_AUTO_APPROVE') == '1':
            print("[自动确认: 是]")
            return True
        
        response = input("确认授权? (y/n): ").strip().lower()
        return response in ('y', 'yes', '是', '1')
    
    return callback
