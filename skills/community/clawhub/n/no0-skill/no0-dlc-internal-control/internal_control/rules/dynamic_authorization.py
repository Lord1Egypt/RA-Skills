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
from .dynamic_models import DynamicClassificationResult, get_level_strictness

# 导入 HTTP 授权服务
from ..http_auth import HTTPAuthService, AuthRequest, AuthStatus

# 导入 TOTP Vault
from ..totp_vault import TOTPVault, MFAResult
from ..totp_vault.integration import MFAuthorizationProvider

logger = logging.getLogger(__name__)


class AuthorizationStrategy(Enum):
    """授权策略枚举"""
    NONE = "none"                    # 无需授权
    HTTP_ONLY = "http_only"          # 仅 HTTP 授权
    TOTP_ONLY = "totp_only"          # 仅 TOTP MFA
    HTTP_THEN_TOTP = "http_then_totp"  # HTTP + TOTP 两步授权
    DENY = "deny"                    # 直接拒绝


@dataclass
class AuthorizationChain:
    """
    授权链
    
    定义完成访问授权所需的步骤
    """
    strategy: AuthorizationStrategy
    steps: List[Dict[str, Any]] = field(default_factory=list)
    current_step: int = 0
    is_complete: bool = False
    final_result: Optional[AccessDecision] = None
    
    def get_current_step(self) -> Optional[Dict[str, Any]]:
        """获取当前步骤"""
        if self.current_step < len(self.steps):
            return self.steps[self.current_step]
        return None
    
    def advance(self) -> bool:
        """进入下一步"""
        self.current_step += 1
        if self.current_step >= len(self.steps):
            self.is_complete = True
            return False
        return True


@dataclass
class DynamicAuthorizationConfig:
    """
    动态授权配置
    
    定义不同级别对应的授权策略
    """
    # 级别到策略的映射
    level_strategies: Dict[DataLevel, AuthorizationStrategy] = field(default_factory=dict)
    
    # 批量升级额外要求
    bulk_upgrade_requires_mfa: bool = True  # 批量升级是否强制 MFA
    
    # 跨域传输额外要求
    cross_domain_requires_mfa: bool = True  # 跨境传输强制 MFA
    
    # 授权缓存配置
    auth_cache_ttl: int = 300  # 授权缓存时间（秒）
    
    # TOTP 配置
    totp_auto_approve: bool = False  # 是否自动批准 TOTP（演示模式）
    
    def __post_init__(self):
        """初始化默认配置"""
        if not self.level_strategies:
            self.level_strategies = {
                DataLevel.L1_PUBLIC: AuthorizationStrategy.NONE,
                DataLevel.L2_INTERNAL: AuthorizationStrategy.NONE,
                DataLevel.L3_RESTRICTED: AuthorizationStrategy.HTTP_ONLY,
                DataLevel.L4_CONFIDENTIAL: AuthorizationStrategy.HTTP_THEN_TOTP,
                DataLevel.L5_SECRET: AuthorizationStrategy.HTTP_THEN_TOTP,
                DataLevel.L6_CRITICAL: AuthorizationStrategy.DENY,
            }


class DynamicAuthorizationEngine:
    """
    动态授权引擎
    
    根据动态分级结果编排授权流程
    """
    
    def __init__(
        self,
        http_service: HTTPAuthService,
        totp_vault: TOTPVault,
        config: Optional[DynamicAuthorizationConfig] = None
    ):
        self.http_service = http_service
        self.totp_vault = totp_vault
        self.config = config or DynamicAuthorizationConfig()
        
        # MFA 提供者
        self.mfa_provider = MFAuthorizationProvider(totp_vault)
        
        # 授权缓存（避免重复授权）
        self._auth_cache: Dict[str, Dict[str, Any]] = {}
        
        # 回调函数
        self._http_confirmation_callback: Optional[Callable[[str, str], bool]] = None
        self._mfa_confirmation_callback: Optional[Callable[[dict], bool]] = None
    
    def set_http_confirmation_callback(self, callback: Callable[[str, str], bool]) -> None:
        """设置 HTTP 授权确认回调"""
        self._http_confirmation_callback = callback
    
    def set_mfa_confirmation_callback(self, callback: Callable[[dict], bool]) -> None:
        """设置 MFA 确认回调"""
        self._mfa_confirmation_callback = callback
        self.mfa_provider.set_confirmation_callback(callback)
    
    # ========== 核心接口 ==========
    
    async def authorize(
        self,
        agent_id: str,
        resource_path: str,
        operation: AccessOperation,
        dynamic_result: DynamicClassificationResult,
        context: Optional[Dict[str, Any]] = None
    ) -> AccessResult:
        """
        根据动态分级结果执行授权
        
        流程：
        1. 确定授权策略
        2. 检查授权缓存
        3. 执行授权链
        4. 缓存授权结果
        
        Args:
            agent_id: Agent ID
            resource_path: 资源路径
            operation: 操作类型
            dynamic_result: 动态分级结果
            context: 额外上下文
            
        Returns:
            访问决策结果
        """
        # 1. 确定授权策略
        strategy = self._determine_strategy(dynamic_result, context)
        
        logger.info(
            f"动态授权: {agent_id} -> {resource_path} "
            f"[级别: {dynamic_result.adjusted_level.value}, "
            f"策略: {strategy.value}]"
        )
        
        # 2. 检查缓存
        cache_key = self._build_cache_key(agent_id, resource_path, dynamic_result)
        if self._check_cache(cache_key):
            logger.debug(f"授权缓存命中: {cache_key}")
            return AccessResult(
                decision=AccessDecision.ALLOW,
                token=self._auth_cache[cache_key]['token'],
                expires_at=self._auth_cache[cache_key]['expires_at'],
                level=dynamic_result.adjusted_level,
                policy=strategy.value,
                reason="授权缓存有效",
                audit_record_id=""
            )
        
        # 3. 根据策略执行授权
        if strategy == AuthorizationStrategy.NONE:
            return await self._grant_direct(dynamic_result)
        
        elif strategy == AuthorizationStrategy.HTTP_ONLY:
            return await self._execute_http_auth(
                agent_id, resource_path, operation, dynamic_result, context
            )
        
        elif strategy == AuthorizationStrategy.TOTP_ONLY:
            return await self._execute_totp_auth(
                agent_id, resource_path, operation, dynamic_result
            )
        
        elif strategy == AuthorizationStrategy.HTTP_THEN_TOTP:
            return await self._execute_http_then_totp(
                agent_id, resource_path, operation, dynamic_result, context
            )
        
        elif strategy == AuthorizationStrategy.DENY:
            return await self._deny_access(dynamic_result, "级别过高，禁止访问")
        
        else:
            return await self._deny_access(dynamic_result, f"未知授权策略: {strategy}")
    
    def _determine_strategy(
        self,
        dynamic_result: DynamicClassificationResult,
        context: Optional[Dict[str, Any]]
    ) -> AuthorizationStrategy:
        """
        确定授权策略
        
        考虑因素：
        - 基础级别策略
        - 批量升级（强制 MFA）
        - 跨域传输（强制 MFA）
        """
        level = dynamic_result.adjusted_level
        base_strategy = self.config.level_strategies.get(level, AuthorizationStrategy.DENY)
        
        # 如果基础策略已经是 MFA 或拒绝，直接返回
        if base_strategy in [AuthorizationStrategy.TOTP_ONLY, 
                             AuthorizationStrategy.HTTP_THEN_TOTP,
                             AuthorizationStrategy.DENY]:
            return base_strategy
        
        # 检查是否需要增强授权（批量升级）
        if context:
            # 批量升级场景
            if context.get('is_bulk_upgrade') and self.config.bulk_upgrade_requires_mfa:
                if base_strategy == AuthorizationStrategy.HTTP_ONLY:
                    return AuthorizationStrategy.HTTP_THEN_TOTP
            
            # 跨域传输场景
            if context.get('is_cross_domain') and self.config.cross_domain_requires_mfa:
                if base_strategy == AuthorizationStrategy.HTTP_ONLY:
                    return AuthorizationStrategy.HTTP_THEN_TOTP
        
        return base_strategy
    
    # ========== 授权执行 ==========
    
    async def _execute_http_auth(
        self,
        agent_id: str,
        resource_path: str,
        operation: AccessOperation,
        dynamic_result: DynamicClassificationResult,
        context: Optional[Dict[str, Any]]
    ) -> AccessResult:
        """执行 HTTP 授权"""
        try:
            # 创建 HTTP 授权请求
            request_id = self.http_service.create_auth_request(
                agent_id=agent_id,
                resource_path=resource_path,
                operation=operation.value.upper(),
                data_level=dynamic_result.adjusted_level.value,
                context={
                    **(context or {}),
                    "adjustment_type": dynamic_result.adjustment_type,
                    "adjustment_reason": dynamic_result.adjustment_reason,
                    "applied_rules": dynamic_result.applied_rules
                },
                timeout_seconds=120
            )
            
            logger.info(f"HTTP 授权请求创建: {request_id}")
            
            # 获取授权 URL
            auth_url = f"http://localhost:{self.http_service.port}/ui/auth/{request_id}"
            
            # 触发回调（如打开浏览器）
            if self._http_confirmation_callback:
                approved = self._http_confirmation_callback(auth_url, request_id)
                if not approved:
                    return await self._deny_access(dynamic_result, "用户拒绝 HTTP 授权")
            
            # 轮询等待授权结果
            auth_result = await self._poll_http_auth(request_id, timeout=120)
            
            if auth_result == AuthStatus.CONFIRMED:
                # 授权成功
                token = f"http-auth-{request_id}"
                self._cache_auth(agent_id, resource_path, dynamic_result, token)
                
                return AccessResult(
                    decision=AccessDecision.ALLOW,
                    token=token,
                    expires_at=datetime.now() + timedelta(minutes=5),
                    level=dynamic_result.adjusted_level,
                    policy="http_authorized",
                    reason="HTTP 授权通过",
                    audit_record_id=f"audit-http-{request_id}"
                )
            else:
                return await self._deny_access(dynamic_result, f"HTTP 授权失败: {auth_result}")
                
        except Exception as e:
            logger.error(f"HTTP 授权异常: {e}")
            return await self._deny_access(dynamic_result, f"HTTP 授权异常: {e}")
    
    async def _execute_totp_auth(
        self,
        agent_id: str,
        resource_path: str,
        operation: AccessOperation,
        dynamic_result: DynamicClassificationResult
    ) -> AccessResult:
        """执行 TOTP MFA 授权"""
        try:
            # 获取对应级别的 TOTP 上下文
            level_context = dynamic_result.adjusted_level.value.lower().replace("-", "_")
            
            # 获取或创建 TOTP 密钥
            from ..totp_vault.models import KeyStatus
            key_meta = self.totp_vault.get_key_by_context(level_context)
            
            if not key_meta:
                # 首次使用，生成密钥
                key_meta = self.totp_vault.generate_key(context=level_context)
                logger.info(f"生成 TOTP 密钥: {key_meta.key_id} for {level_context}")
            
            # 执行 MFA 流程
            mfa_result = self.totp_vault.execute_mfa_flow(
                key_id=key_meta.key_id,
                human_confirmation_callback=self._mfa_confirmation_callback
            )
            
            if mfa_result.granted:
                # MFA 通过
                token = f"totp-auth-{key_meta.key_id}"
                self._cache_auth(agent_id, resource_path, dynamic_result, token)
                
                return AccessResult(
                    decision=AccessDecision.ALLOW,
                    token=token,
                    expires_at=datetime.now() + timedelta(minutes=5),
                    level=dynamic_result.adjusted_level,
                    policy="totp_authorized",
                    reason=f"TOTP MFA 授权通过: {mfa_result.message}",
                    audit_record_id=f"audit-totp-{key_meta.key_id}"
                )
            else:
                return await self._deny_access(dynamic_result, f"TOTP MFA 失败: {mfa_result.message}")
                
        except Exception as e:
            logger.error(f"TOTP 授权异常: {e}")
            return await self._deny_access(dynamic_result, f"TOTP 授权异常: {e}")
    
    async def _execute_http_then_totp(
        self,
        agent_id: str,
        resource_path: str,
        operation: AccessOperation,
        dynamic_result: DynamicClassificationResult,
        context: Optional[Dict[str, Any]]
    ) -> AccessResult:
        """执行 HTTP + TOTP 两步授权"""
        # 第一步：HTTP 授权
        logger.info("两步授权: 开始 HTTP 授权")
        http_result = await self._execute_http_auth(
            agent_id, resource_path, operation, dynamic_result, context
        )
        
        if http_result.decision != AccessDecision.ALLOW:
            return http_result
        
        # 第二步：TOTP 授权
        logger.info("两步授权: HTTP 通过，开始 TOTP MFA")
        totp_result = await self._execute_totp_auth(
            agent_id, resource_path, operation, dynamic_result
        )
        
        if totp_result.decision == AccessDecision.ALLOW:
            # 两步都通过
            return AccessResult(
                decision=AccessDecision.ALLOW,
                token=f"dual-auth-{http_result.token}-{totp_result.token}",
                expires_at=totp_result.expires_at,
                level=dynamic_result.adjusted_level,
                policy="http_then_totp_authorized",
                reason="HTTP 授权 + TOTP MFA 两步验证通过",
                audit_record_id=f"{http_result.audit_record_id},{totp_result.audit_record_id}"
            )
        else:
            return totp_result
    
    # ========== 辅助方法 ==========
    
    async def _poll_http_auth(self, request_id: str, timeout: int = 120) -> str:
        """轮询 HTTP 授权状态"""
        import time
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            status = self.http_service.get_auth_status(request_id)
            if status in [AuthStatus.CONFIRMED, AuthStatus.DENIED, AuthStatus.EXPIRED]:
                return status
            await asyncio.sleep(1)
        
        return AuthStatus.EXPIRED
    
    def _build_cache_key(
        self,
        agent_id: str,
        resource_path: str,
        dynamic_result: DynamicClassificationResult
    ) -> str:
        """构建缓存键"""
        return f"{agent_id}:{resource_path}:{dynamic_result.adjusted_level.value}"
    
    def _check_cache(self, cache_key: str) -> bool:
        """检查授权缓存"""
        if cache_key not in self._auth_cache:
            return False
        
        cached = self._auth_cache[cache_key]
        if datetime.now() > cached['expires_at']:
            # 缓存过期
            del self._auth_cache[cache_key]
            return False
        
        return True
    
    def _cache_auth(
        self,
        agent_id: str,
        resource_path: str,
        dynamic_result: DynamicClassificationResult,
        token: str
    ) -> None:
        """缓存授权结果"""
        cache_key = self._build_cache_key(agent_id, resource_path, dynamic_result)
        self._auth_cache[cache_key] = {
            'token': token,
            'expires_at': datetime.now() + timedelta(seconds=self.config.auth_cache_ttl),
            'level': dynamic_result.adjusted_level.value
        }
    
    async def _grant_direct(self, dynamic_result: DynamicClassificationResult) -> AccessResult:
        """直接授予访问权限"""
        return AccessResult(
            decision=AccessDecision.ALLOW,
            token="direct-grant",
            expires_at=datetime.now() + timedelta(minutes=5),
            level=dynamic_result.adjusted_level,
            policy="direct",
            reason="无需授权",
            audit_record_id=""
        )
    
    async def _deny_access(
        self,
        dynamic_result: DynamicClassificationResult,
        reason: str
    ) -> AccessResult:
        """拒绝访问"""
        return AccessResult(
            decision=AccessDecision.DENY,
            token=None,
            expires_at=None,
            level=dynamic_result.adjusted_level,
            policy="deny",
            reason=reason,
            audit_record_id=""
        )
    
    def clear_cache(self) -> None:
        """清除授权缓存"""
        self._auth_cache.clear()
        logger.info("授权缓存已清除")
