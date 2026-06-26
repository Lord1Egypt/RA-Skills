"""
动态分级与 Reference Monitor 集成模块

职责：
1. 在 Reference Monitor 访问控制流程中引入动态分级
2. 支持批量操作的动态汇聚升级
3. 支持脱敏后的动态降级
4. 审计日志记录动态分级调整
5. 提供上下文感知的访问控制
"""

import asyncio
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple
from pathlib import Path
from enum import Enum

# 导入 Reference Monitor 组件
from ..reference_monitor import (
    ReferenceMonitor,
    Agent,
    AccessOperation,
    AccessDecision,
    AccessRequest,
    AccessResult,
    Classification,
    PolicyDecision,
    DataLevel,
    AuditEventType
)

# 导入动态分级组件
from .dynamic_engine import DynamicClassificationEngine
from .dynamic_models import (
    DynamicClassificationContext,
    DynamicClassificationResult,
    AggregationType,
    DesensitizationMethod
)

# 导入静态分级组件
from .engine import ClassificationEngine
from .models import ClassificationResult

logger = logging.getLogger(__name__)


class DynamicAccessContext:
    """
    动态访问上下文
    
    封装影响访问控制决策的动态因素
    """
    
    def __init__(
        self,
        # 基础信息
        agent_id: str,
        operation: AccessOperation,
        
        # 批量操作信息
        is_bulk_operation: bool = False,
        bulk_record_count: int = 1,
        bulk_paths: Optional[List[str]] = None,
        aggregation_type: AggregationType = AggregationType.BATCH_QUERY,
        
        # 脱敏信息
        is_desensitized: bool = False,
        desensitization_methods: Optional[List[DesensitizationMethod]] = None,
        
        # 关联信息
        correlated_fields: Optional[List[str]] = None,
        correlation_score: float = 0.0,
        can_identify_individual: bool = False,
        
        # 传输信息
        destination: Optional[str] = None,  # 'internal', 'external_cloud', 'external_overseas'
        
        # 时间信息
        data_created_at: Optional[datetime] = None,
        has_incident_history: bool = False,
        
        # 额外上下文
        extra: Optional[Dict[str, Any]] = None
    ):
        self.agent_id = agent_id
        self.operation = operation
        
        # 批量操作
        self.is_bulk_operation = is_bulk_operation
        self.bulk_record_count = bulk_record_count
        self.bulk_paths = bulk_paths or []
        self.aggregation_type = aggregation_type
        
        # 脱敏
        self.is_desensitized = is_desensitized
        self.desensitization_methods = desensitization_methods or []
        
        # 关联
        self.correlated_fields = correlated_fields or []
        self.correlation_score = correlation_score
        self.can_identify_individual = can_identify_individual
        
        # 传输
        self.destination = destination
        
        # 时间
        self.data_created_at = data_created_at
        self.has_incident_history = has_incident_history
        
        # 额外
        self.extra = extra or {}
    
    def to_classification_context(
        self,
        base_classification: ClassificationResult
    ) -> DynamicClassificationContext:
        """转换为动态分级上下文"""
        return DynamicClassificationContext(
            base_classification=base_classification,
            record_count=self.bulk_record_count if self.is_bulk_operation else 1,
            aggregation_type=self.aggregation_type if self.is_bulk_operation else None,
            is_desensitized=self.is_desensitized,
            desensitization_methods=self.desensitization_methods,
            correlated_fields=self.correlated_fields,
            correlation_score=self.correlation_score,
            can_identify_individual=self.can_identify_individual,
            destination=self.destination,
            data_created_at=self.data_created_at,
            context_source="access_control"
        )


class DynamicClassificationAccessMonitor(ReferenceMonitor):
    """
    支持动态分级的 Reference Monitor
    
    扩展 ReferenceMonitor，添加动态分级能力：
    - 批量操作时自动汇聚升级
    - 脱敏后自动降级
    - 时间衰减自动降级
    - 关联增强自动升级
    """
    
    def __init__(self):
        super().__init__()
        self.dynamic_engine = DynamicClassificationEngine()
        
        # 批量操作状态跟踪
        self._bulk_operation_contexts: Dict[str, DynamicAccessContext] = {}
    
    async def check_access_with_dynamic_context(
        self,
        agent_id: str,
        file_path: str,
        operation: AccessOperation,
        dynamic_context: DynamicAccessContext,
        base_context: Optional[Dict[str, Any]] = None
    ) -> AccessResult:
        """
        带动态上下文的访问控制检查
        
        流程：
        1. 获取基础分级（静态规则）
        2. 应用动态分级调整
        3. 基于调整后级别进行访问控制决策
        4. 记录审计日志（包含动态调整信息）
        
        Args:
            agent_id: Agent ID
            file_path: 文件路径
            operation: 操作类型
            dynamic_context: 动态访问上下文
            base_context: 基础上下文
            
        Returns:
            访问决策结果
        """
        request = AccessRequest(
            agent_id=agent_id,
            file_path=file_path,
            operation=operation,
            context=base_context or {},
            timestamp=datetime.now()
        )
        
        try:
            # 1. Agent 身份验证
            agent = await self._authenticate_agent(agent_id)
            if not agent:
                return await self._deny_access(request, "Agent authentication failed")
            
            # 2. 获取基础分级
            base_classification = await self._get_classification(file_path)
            
            # 3. 应用动态分级
            adjusted_classification, dynamic_result = await self._apply_dynamic_classification(
                base_classification, dynamic_context
            )
            
            # 4. 评估访问策略（使用调整后的分级）
            policy_decision = await self._evaluate_policy(
                agent, adjusted_classification, operation, base_context or {}
            )
            
            # 5. 记录审计日志（包含动态调整信息）
            audit_record_id = await self._log_with_dynamic_adjustment(
                request, base_classification, adjusted_classification, 
                dynamic_result, policy_decision
            )
            
            # 6. 构建结果
            return await self._build_dynamic_result(
                request, adjusted_classification, policy_decision, 
                audit_record_id, dynamic_result
            )
            
        except Exception as e:
            return await self._handle_error(request, e)
    
    async def check_bulk_access(
        self,
        agent_id: str,
        file_paths: List[str],
        operation: AccessOperation,
        aggregation_type: AggregationType = AggregationType.BULK_EXPORT,
        base_context: Optional[Dict[str, Any]] = None
    ) -> Tuple[List[AccessResult], Dict[str, Any]]:
        """
        批量访问控制检查（自动应用汇聚升级）
        
        Args:
            agent_id: Agent ID
            file_paths: 文件路径列表
            operation: 操作类型
            aggregation_type: 汇聚类型
            base_context: 基础上下文
            
        Returns:
            (访问决策结果列表, 汇总统计)
        """
        if not file_paths:
            return [], {"total": 0, "allowed": 0, "denied": 0, "upgraded": 0}
        
        # 1. 获取所有路径的基础分级
        base_classifications = []
        for path in file_paths:
            classification = await self._get_classification(path)
            base_classifications.append(classification)
        
        # 2. 按级别分组，计算每组的动态调整
        from collections import defaultdict
        level_groups = defaultdict(list)
        for i, classification in enumerate(base_classifications):
            level_groups[classification.level].append((i, classification))
        
        # 3. 对每组应用汇聚升级
        adjusted_classifications = [None] * len(file_paths)
        dynamic_results = [None] * len(file_paths)
        
        for base_level, items in level_groups.items():
            # 构建批量动态上下文
            bulk_context = DynamicAccessContext(
                agent_id=agent_id,
                operation=operation,
                is_bulk_operation=True,
                bulk_record_count=len(items),
                bulk_paths=[file_paths[i] for i, _ in items],
                aggregation_type=aggregation_type
            )
            
            # 检查该组是否需要升级
            for idx, (original_idx, base_classification) in enumerate(items):
                # 构建 ClassificationResult
                base_result = ClassificationResult(
                    path=base_classification.path,
                    level=base_classification.level.value,
                    source=base_classification.source,
                    confidence=base_classification.confidence,
                    reason=base_classification.reason
                )
                
                # 应用动态分级
                classification_context = bulk_context.to_classification_context(base_result)
                dynamic_result = await self.dynamic_engine.classify_with_context(
                    base_result, classification_context
                )
                
                # 转换为 Classification
                adjusted_classification = Classification(
                    path=base_classification.path,
                    level=dynamic_result.adjusted_level,
                    source=f"dynamic_{dynamic_result.adjustment_type.lower()}",
                    confidence=base_classification.confidence,
                    reason=f"{base_classification.reason} -> {dynamic_result.adjustment_reason}"
                )
                
                adjusted_classifications[original_idx] = adjusted_classification
                dynamic_results[original_idx] = dynamic_result
        
        # 4. 对每个路径进行访问控制检查
        results = []
        stats = {"total": len(file_paths), "allowed": 0, "denied": 0, "upgraded": 0}
        
        agent = await self._authenticate_agent(agent_id)
        
        for i, (path, adjusted_classification, dynamic_result) in enumerate(
            zip(file_paths, adjusted_classifications, dynamic_results)
        ):
            request = AccessRequest(
                agent_id=agent_id,
                file_path=path,
                operation=operation,
                context=base_context or {},
                timestamp=datetime.now()
            )
            
            if not agent:
                result = await self._deny_access(request, "Agent authentication failed")
            else:
                # 评估策略
                policy_decision = await self._evaluate_policy(
                    agent, adjusted_classification, operation, base_context or {}
                )
                
                # 记录审计
                audit_record_id = await self._log_with_dynamic_adjustment(
                    request, base_classifications[i], adjusted_classification,
                    dynamic_result, policy_decision
                )
                
                # 构建结果
                result = await self._build_dynamic_result(
                    request, adjusted_classification, policy_decision,
                    audit_record_id, dynamic_result
                )
            
            results.append(result)
            
            # 统计
            if result.decision == AccessDecision.ALLOW:
                stats["allowed"] += 1
            else:
                stats["denied"] += 1
            
            if dynamic_result.adjustment_type == "UPGRADE":
                stats["upgraded"] += 1
        
        return results, stats
    
    async def check_desensitized_access(
        self,
        agent_id: str,
        file_path: str,
        original_level: DataLevel,
        desensitization_methods: List[DesensitizationMethod],
        operation: AccessOperation = AccessOperation.READ,
        base_context: Optional[Dict[str, Any]] = None
    ) -> AccessResult:
        """
        脱敏数据的访问控制检查（自动应用降级）
        
        Args:
            agent_id: Agent ID
            file_path: 文件路径
            original_level: 原始分级级别
            desensitization_methods: 应用的脱敏方法
            operation: 操作类型
            base_context: 基础上下文
            
        Returns:
            访问决策结果
        """
        # 构建动态上下文
        dynamic_context = DynamicAccessContext(
            agent_id=agent_id,
            operation=operation,
            is_desensitized=True,
            desensitization_methods=desensitization_methods
        )
        
        # 使用原始级别作为基础分级
        base_classification = Classification(
            path=file_path,
            level=original_level,
            source="manual",
            confidence=1.0,
            reason="原始分级（脱敏前）"
        )
        
        request = AccessRequest(
            agent_id=agent_id,
            file_path=file_path,
            operation=operation,
            context=base_context or {},
            timestamp=datetime.now()
        )
        
        try:
            # Agent 验证
            agent = await self._authenticate_agent(agent_id)
            if not agent:
                return await self._deny_access(request, "Agent authentication failed")
            
            # 应用动态分级（脱敏降级）
            adjusted_classification, dynamic_result = await self._apply_dynamic_classification(
                base_classification, dynamic_context
            )
            
            # 评估策略
            policy_decision = await self._evaluate_policy(
                agent, adjusted_classification, operation, base_context or {}
            )
            
            # 记录审计
            audit_record_id = await self._log_with_dynamic_adjustment(
                request, base_classification, adjusted_classification,
                dynamic_result, policy_decision
            )
            
            # 构建结果
            return await self._build_dynamic_result(
                request, adjusted_classification, policy_decision,
                audit_record_id, dynamic_result
            )
            
        except Exception as e:
            return await self._handle_error(request, e)
    
    async def _apply_dynamic_classification(
        self,
        base_classification: Classification,
        dynamic_context: DynamicAccessContext
    ) -> Tuple[Classification, DynamicClassificationResult]:
        """
        应用动态分级
        
        Returns:
            (调整后的分级, 动态分级结果)
        """
        # 转换为 ClassificationResult
        base_result = ClassificationResult(
            path=base_classification.path,
            level=base_classification.level.value,
            source=base_classification.source,
            confidence=base_classification.confidence,
            reason=base_classification.reason
        )
        
        # 转换为动态分级上下文
        classification_context = dynamic_context.to_classification_context(base_result)
        
        # 应用动态分级
        dynamic_result = await self.dynamic_engine.classify_with_context(
            base_result, classification_context
        )
        
        # 转换为 Classification
        adjusted_classification = Classification(
            path=base_classification.path,
            level=dynamic_result.adjusted_level,
            source=f"dynamic_{dynamic_result.adjustment_type.lower()}",
            confidence=base_classification.confidence,
            reason=f"{base_classification.reason} -> {dynamic_result.adjustment_reason}"
        )
        
        return adjusted_classification, dynamic_result
    
    async def _log_with_dynamic_adjustment(
        self,
        request: AccessRequest,
        base_classification: Classification,
        adjusted_classification: Classification,
        dynamic_result: DynamicClassificationResult,
        policy_decision: PolicyDecision
    ) -> str:
        """
        记录包含动态调整的审计日志
        
        扩展标准审计日志，添加动态分级信息
        """
        # 构建增强的审计记录
        audit_context = {
            "base_level": base_classification.level.value,
            "adjusted_level": adjusted_classification.level.value,
            "adjustment_type": dynamic_result.adjustment_type,
            "adjustment_reason": dynamic_result.adjustment_reason,
            "applied_rules": dynamic_result.applied_rules,
            "dynamic_context": {
                "record_count": dynamic_result.context.record_count,
                "is_desensitized": dynamic_result.context.is_desensitized,
                "correlation_score": dynamic_result.context.correlation_score,
                "destination": dynamic_result.context.destination
            }
        }
        
        # 创建增强的 PolicyDecision
        enhanced_decision = PolicyDecision(
            decision=policy_decision.decision,
            reason=f"{policy_decision.reason} [动态调整: {dynamic_result.adjustment_type}]",
            requires_auth=policy_decision.requires_auth,
            auth_method=policy_decision.auth_method
        )
        
        # 记录审计日志
        return await self.audit_logger.log_access_request(
            request, adjusted_classification, enhanced_decision
        )
    
    async def _build_dynamic_result(
        self,
        request: AccessRequest,
        classification: Classification,
        policy_decision: PolicyDecision,
        audit_record_id: str,
        dynamic_result: DynamicClassificationResult
    ) -> AccessResult:
        """
        构建包含动态分级信息的结果
        """
        result = AccessResult(
            decision=policy_decision.decision,
            token=None,  # 如需授权，在外部生成
            expires_at=None,
            level=classification.level,
            policy=policy_decision.auth_method or "direct",
            reason=policy_decision.reason,
            audit_record_id=audit_record_id
        )
        
        # 添加动态分级元数据（便于上层应用使用）
        result._dynamic_metadata = {
            "adjustment_type": dynamic_result.adjustment_type,
            "adjustment_reason": dynamic_result.adjustment_reason,
            "applied_rules": dynamic_result.applied_rules,
            "base_level": dynamic_result.original_result.level
        }
        
        return result
    
    def get_dynamic_adjustment_info(self, result: AccessResult) -> Optional[Dict[str, Any]]:
        """获取结果的动态分级调整信息"""
        return getattr(result, '_dynamic_metadata', None)


class DynamicAccessMonitorFactory:
    """
    动态访问监控器工厂
    
    提供便捷的创建和配置方法
    """
    
    @staticmethod
    def create_standard_monitor() -> DynamicClassificationAccessMonitor:
        """创建标准配置的监控器"""
        monitor = DynamicClassificationAccessMonitor()
        return monitor
    
    @staticmethod
    def create_strict_monitor() -> DynamicClassificationAccessMonitor:
        """创建严格模式的监控器（更敏感的动态调整）"""
        monitor = DynamicClassificationAccessMonitor()
        
        # 添加更严格的汇聚规则
        from .dynamic_models import DynamicRule, DynamicRuleType
        
        strict_rule = DynamicRule(
            id="strict_agg_l2_to_l3",
            name="严格L2汇聚升级",
            rule_type=DynamicRuleType.AGGREGATION_UPGRADE,
            condition=lambda ctx: (
                ctx.get_effective_level() == DataLevel.L2_INTERNAL and
                ctx.record_count >= 50  # 更严格的阈值
            ),
            action="UPGRADE",
            target_level=DataLevel.L3_RESTRICTED,
            applicable_levels=[DataLevel.L2_INTERNAL],
            description="L2数据超过50条即升级为L3",
            priority=5
        )
        
        monitor.dynamic_engine.add_rule(strict_rule)
        
        return monitor
    
    @staticmethod
    def create_permissive_monitor() -> DynamicClassificationAccessMonitor:
        """创建宽松模式的监控器（更宽松的动态调整）"""
        monitor = DynamicClassificationAccessMonitor()
        
        # 禁用一些降级规则
        monitor.dynamic_engine.disable_rule("desens_phone_l3_to_l2")
        
        return monitor
