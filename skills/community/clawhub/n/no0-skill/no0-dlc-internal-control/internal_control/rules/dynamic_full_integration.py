"""
动态分级 + HTTP授权 + TOTP MFA 完整联动集成

这是完整的端到端集成：
1. 动态分级引擎调整数据级别
2. 根据级别选择授权策略
3. 执行 HTTP / TOTP / HTTP+TOTP 授权
4. 返回最终访问决策
"""

import asyncio
import logging
from datetime import datetime
from typing import Optional, Dict, Any, Callable
from pathlib import Path

from ..reference_monitor import (
    AccessOperation, AccessDecision, AccessResult, DataLevel
)
from .dynamic_integration import (
    DynamicClassificationAccessMonitor, DynamicAccessContext
)
from .dynamic_models import DynamicClassificationResult
from .dynamic_authorization import (
    DynamicAuthorizationEngine, DynamicAuthorizationConfig, AuthorizationStrategy
)

# 导入 HTTP 服务
from ..http_auth import HTTPAuthService

# 导入 TOTP Vault
from ..totp_vault import TOTPVault, MasterKeyManager

logger = logging.getLogger(__name__)


class DynamicAuthorizationAccessMonitor(DynamicClassificationAccessMonitor):
    """
    支持动态分级 + 完整授权链的 Reference Monitor
    
    这是终极集成版本：
    - 动态分级（汇聚升级、脱敏降级）
    - 策略选择（L3=HTTP, L4+=HTTP+TOTP）
    - 授权执行（HTTP服务、TOTP Vault）
    - 决策返回（含完整审计链）
    """
    
    def __init__(self, auth_config: Optional[DynamicAuthorizationConfig] = None):
        super().__init__()
        
        # HTTP 服务
        self.http_service: Optional[HTTPAuthService] = None
        self._http_port: int = 0
        
        # TOTP Vault
        self.totp_vault: Optional[TOTPVault] = None
        self._master_key_manager = MasterKeyManager()
        
        # 授权引擎
        self.auth_config = auth_config or DynamicAuthorizationConfig()
        self.auth_engine: Optional[DynamicAuthorizationEngine] = None
        
        # 回调函数
        self._auto_approve: bool = False  # 演示模式自动批准
    
    async def initialize(self, http_port: int = 0, totp_password: str = "demo-password"):
        """
        初始化完整联动系统
        
        Args:
            http_port: HTTP 服务端口（0=随机）
            totp_password: TOTP Vault 主密码
        """
        print("\n" + "="*70)
        print("🚀 初始化动态分级 + 授权联动系统")
        print("="*70)
        
        # 1. 初始化父类（Reference Monitor）
        await super().initialize()
        print("✅ Reference Monitor 初始化完成")
        
        # 2. 初始化 HTTP 授权服务
        print("\n[1/3] 初始化 HTTP 授权服务...")
        self.http_service = HTTPAuthService(port=http_port)
        self._http_port = self.http_service.start()
        print(f"   ✅ HTTP 服务启动 @ http://127.0.0.1:{self._http_port}")
        
        # 3. 初始化 TOTP Vault
        print("\n[2/3] 初始化 TOTP Vault...")
        if not self._master_key_manager.is_initialized():
            master_key = self._master_key_manager.initialize(totp_password)
        else:
            master_key = self._master_key_manager.unlock(totp_password)
        
        self.totp_vault = TOTPVault(master_key=master_key)
        
        # 预生成各级别 TOTP 密钥
        for level in ["l3_restricted", "l4_confidential", "l5_secret"]:
            existing = self.totp_vault.get_key_by_context(level)
            if not existing:
                self.totp_vault.generate_key(context=level)
                print(f"   ✓ 生成 {level} TOTP 密钥")
        
        print("   ✅ TOTP Vault 初始化完成")
        
        # 4. 初始化授权引擎
        print("\n[3/3] 初始化授权引擎...")
        self.auth_engine = DynamicAuthorizationEngine(
            http_service=self.http_service,
            totp_vault=self.totp_vault,
            config=self.auth_config
        )
        
        # 设置回调
        self._setup_callbacks()
        
        print("   ✅ 授权引擎初始化完成")
        print("\n" + "="*70)
        print("🎯 联动系统初始化完成！")
        print("="*70)
    
    def _setup_callbacks(self) -> None:
        """设置授权确认回调"""
        # HTTP 授权回调
        def http_callback(auth_url: str, request_id: str) -> bool:
            print(f"\n   🔐 HTTP 授权请求")
            print(f"      页面: {auth_url}")
            
            if self._auto_approve:
                print(f"      [演示模式] 3秒后自动批准...")
                import time
                time.sleep(3)
                self.http_service.confirm_auth(request_id, "demo_user")
                return True
            
            # 实际场景：打开浏览器等待用户确认
            import webbrowser
            webbrowser.open(auth_url)
            return True
        
        # MFA 回调
        def mfa_callback(request_info: dict) -> bool:
            print(f"\n   🔑 TOTP MFA 请求")
            print(f"      上下文: {request_info['context']}")
            
            if self._auto_approve:
                print(f"      [演示模式] 自动批准")
                return True
            
            return True
        
        self.auth_engine.set_http_confirmation_callback(http_callback)
        self.auth_engine.set_mfa_confirmation_callback(mfa_callback)
    
    def enable_auto_approve(self, enable: bool = True) -> None:
        """启用/禁用自动批准（演示模式）"""
        self._auto_approve = enable
        self.auth_config.totp_auto_approve = enable
    
    # ========== 核心联动接口 ==========
    
    async def check_access_with_full_pipeline(
        self,
        agent_id: str,
        file_path: str,
        operation: AccessOperation,
        dynamic_context: DynamicAccessContext,
        base_context: Optional[Dict[str, Any]] = None
    ) -> AccessResult:
        """
        完整联动流程：动态分级 → 授权策略 → 授权执行
        
        流程：
        1. 静态分级（父类）
        2. 动态分级调整（Dynamic Engine）
        3. 授权策略选择（根据调整后级别）
        4. 授权执行（HTTP / TOTP / HTTP+TOTP）
        5. 返回决策
        """
        print(f"\n{'='*70}")
        print(f"🔄 完整联动流程: {file_path}")
        print(f"{'='*70}")
        
        # 步骤1: 静态分级
        print("\n📍 Step 1: 静态分级")
        base_classification = await self._get_classification(file_path)
        print(f"   基础级别: {base_classification.level.value}")
        
        # 步骤2: 动态分级调整
        print("\n📍 Step 2: 动态分级调整")
        adjusted_classification, dynamic_result = await self._apply_dynamic_classification(
            base_classification, dynamic_context
        )
        
        print(f"   调整后级别: {adjusted_classification.level.value}")
        print(f"   调整类型: {dynamic_result.adjustment_type}")
        print(f"   调整原因: {dynamic_result.adjustment_reason}")
        
        # 步骤3: 确定授权策略
        strategy = self.auth_engine._determine_strategy(dynamic_result, base_context)
        print(f"\n📍 Step 3: 授权策略选择")
        print(f"   策略: {strategy.value}")
        
        # 步骤4: 执行授权
        print(f"\n📍 Step 4: 执行授权")
        auth_result = await self.auth_engine.authorize(
            agent_id=agent_id,
            resource_path=file_path,
            operation=operation,
            dynamic_result=dynamic_result,
            context=base_context
        )
        
        # 步骤5: 返回结果
        print(f"\n📍 Step 5: 决策结果")
        print(f"   决策: {auth_result.decision.value}")
        print(f"   原因: {auth_result.reason}")
        
        return auth_result
    
    async def check_bulk_with_full_pipeline(
        self,
        agent_id: str,
        file_paths: list,
        operation: AccessOperation,
        aggregation_type: Any,  # AggregationType
        base_context: Optional[Dict[str, Any]] = None
    ) -> tuple:
        """
        批量操作的完整联动流程
        
        特点：
        - 批量汇聚升级后，触发更强的授权要求
        - L2→L3 可能需要 HTTP
        - L3→L4 可能需要 HTTP+TOTP
        """
        print(f"\n{'='*70}")
        print(f"🔄 批量联动流程: {len(file_paths)} 个文件")
        print(f"{'='*70}")
        
        # 批量动态分级
        print("\n📍 Step 1-2: 批量动态分级")
        results, stats = await self.check_bulk_access(
            agent_id=agent_id,
            file_paths=file_paths,
            operation=operation,
            aggregation_type=aggregation_type,
            base_context=base_context
        )
        
        print(f"   汇总: {stats['total']} 文件, {stats['upgraded']} 升级")
        
        # 检查是否有升级的文件需要额外授权
        upgraded_files = [
            (path, result) for path, result in zip(file_paths, results)
            if self.get_dynamic_adjustment_info(result) and
               self.get_dynamic_adjustment_info(result).get('adjustment_type') == 'UPGRADE'
        ]
        
        if upgraded_files:
            print(f"\n📍 Step 3-5: 批量授权")
            print(f"   注意: {len(upgraded_files)} 个文件已升级，需要额外授权")
            
            # 获取升级后的最高级别（使用严格度比较）
            from ..reference_monitor import get_level_strictness
            max_level = max(
                upgraded_files,
                key=lambda x: get_level_strictness(x[1].level.value)
            )[1].level
            
            # 对整个批量操作执行一次授权（而非逐个）
            # 创建模拟的动态结果
            from .dynamic_models import ClassificationResult
            base_result = ClassificationResult(
                path="bulk_operation",
                level=DataLevel.L2_INTERNAL.value,
                source="bulk",
                confidence=1.0,
                reason="批量操作"
            )
            
            dynamic_result = DynamicClassificationResult(
                original_result=base_result,
                adjusted_level=max_level,
                adjustment_type="UPGRADE",
                adjustment_reason=f"批量操作升级，最高级别: {max_level.value}",
                context=None  # 简化
            )
            
            # 执行授权
            auth_result = await self.auth_engine.authorize(
                agent_id=agent_id,
                resource_path=f"bulk://{len(file_paths)}_files",
                operation=operation,
                dynamic_result=dynamic_result,
                context={**base_context, 'is_bulk_upgrade': True}
            )
            
            print(f"   批量授权结果: {auth_result.decision.value}")
            
            # 如果批量授权失败，所有文件都拒绝
            if auth_result.decision != AccessDecision.ALLOW:
                results = [
                    AccessResult(
                        decision=AccessDecision.DENY,
                        token=None,
                        expires_at=None,
                        level=result.level,
                        policy="bulk_denied",
                        reason="批量授权失败",
                        audit_record_id=""
                    ) for result in results
                ]
        
        return results, stats
    
    # ========== 便捷方法 ==========
    
    def get_authorization_summary(self) -> Dict[str, Any]:
        """获取授权系统摘要"""
        return {
            "http_service": {
                "port": self._http_port,
                "running": self.http_service is not None
            },
            "totp_vault": {
                "initialized": self.totp_vault is not None,
                "keys": [
                    k.context for k in self.totp_vault.list_keys()
                ] if self.totp_vault else []
            },
            "auth_engine": {
                "configured": self.auth_engine is not None,
                "strategies": {
                    level.value: strategy.value
                    for level, strategy in self.auth_config.level_strategies.items()
                }
            }
        }
    
    def stop(self) -> None:
        """停止服务"""
        if self.http_service:
            self.http_service.stop()
            print("\n👋 HTTP 服务已停止")


# ========== 工厂函数 ==========

def create_standard_monitor() -> DynamicAuthorizationAccessMonitor:
    """创建标准配置监控器"""
    config = DynamicAuthorizationConfig()
    return DynamicAuthorizationAccessMonitor(config)


def create_strict_monitor() -> DynamicAuthorizationAccessMonitor:
    """创建严格模式监控器"""
    config = DynamicAuthorizationConfig()
    
    # 更严格的策略
    config.level_strategies[DataLevel.L3_RESTRICTED] = AuthorizationStrategy.HTTP_THEN_TOTP
    config.bulk_upgrade_requires_mfa = True
    config.cross_domain_requires_mfa = True
    
    return DynamicAuthorizationAccessMonitor(config)


def create_permissive_monitor() -> DynamicAuthorizationAccessMonitor:
    """创建宽松模式监控器"""
    config = DynamicAuthorizationConfig()
    
    # 更宽松的策略
    config.level_strategies[DataLevel.L4_CONFIDENTIAL] = AuthorizationStrategy.HTTP_ONLY
    config.bulk_upgrade_requires_mfa = False
    
    return DynamicAuthorizationAccessMonitor(config)
