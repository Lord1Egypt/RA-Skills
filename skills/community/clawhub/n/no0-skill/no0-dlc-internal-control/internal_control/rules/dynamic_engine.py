"""
动态分级引擎

职责：
1. 根据上下文动态调整数据分级
2. 支持升级（汇聚、关联）和降级（脱敏、时间衰减）
3. 与静态规则引擎集成
4. 提供审计和追溯能力
"""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple, Any
from pathlib import Path

from .models import DataLevel, ClassificationResult, get_level_strictness
from .dynamic_models import (
    DynamicClassificationContext,
    DynamicClassificationResult,
    DynamicRule,
    AggregationThreshold,
    TimeDecayPolicy,
    AggregationType,
    DesensitizationMethod,
    create_default_dynamic_rules,
    create_default_aggregation_thresholds,
    create_default_time_decay_policies
)

logger = logging.getLogger(__name__)


class DynamicClassificationEngine:
    """
    动态分级引擎
    
    根据动态上下文调整数据分级，支持：
    - 数据汇聚升级
    - 数据脱敏降级
    - 时间衰减降级
    - 关联增强升级
    """
    
    def __init__(self):
        # 规则配置
        self.rules: List[DynamicRule] = []
        self.aggregation_thresholds: List[AggregationThreshold] = []
        self.time_decay_policies: Dict[DataLevel, TimeDecayPolicy] = {}
        
        # 初始化默认配置
        self._load_defaults()
    
    def _load_defaults(self) -> None:
        """加载默认配置"""
        self.rules = create_default_dynamic_rules()
        self.aggregation_thresholds = create_default_aggregation_thresholds()
        
        for policy in create_default_time_decay_policies():
            self.time_decay_policies[policy.applicable_level] = policy
        
        logger.info(f"动态分级引擎初始化完成: {len(self.rules)} 条规则")
    
    # ========== 核心接口 ==========
    
    async def classify_with_context(
        self,
        base_result: ClassificationResult,
        context: DynamicClassificationContext
    ) -> DynamicClassificationResult:
        """
        基于上下文进行动态分级
        
        Args:
            base_result: 基础分级结果（来自静态规则引擎）
            context: 动态分级上下文
            
        Returns:
            动态分级结果（包含调整详情）
        """
        # 评估所有适用规则
        applicable_rules = self._evaluate_rules(context)
        
        if not applicable_rules:
            # 无规则适用，返回原始分级
            return DynamicClassificationResult(
                original_result=base_result,
                adjusted_level=context.get_effective_level(),
                adjustment_type="UNCHANGED",
                adjustment_reason="无动态规则适用",
                context=context
            )
        
        # 计算调整后的级别
        adjusted_level, adjustment_type, reasons = self._calculate_adjusted_level(
            context, applicable_rules
        )
        
        # 构建结果
        result = DynamicClassificationResult(
            original_result=base_result,
            adjusted_level=adjusted_level,
            adjustment_type=adjustment_type,
            adjustment_reason="; ".join(reasons),
            applied_rules=[r.id for r in applicable_rules],
            context=context
        )
        
        logger.debug(
            f"动态分级: {base_result.path} {base_result.level} -> "
            f"{adjusted_level.value} ({adjustment_type})"
        )
        
        return result
    
    def _evaluate_rules(self, context: DynamicClassificationContext) -> List[DynamicRule]:
        """评估所有规则，返回适用的规则列表"""
        applicable = []
        
        for rule in sorted(self.rules, key=lambda r: r.priority):
            if rule.applies_to(context):
                applicable.append(rule)
        
        return applicable
    
    def _calculate_adjusted_level(
        self,
        context: DynamicClassificationContext,
        rules: List[DynamicRule]
    ) -> Tuple[DataLevel, str, List[str]]:
        """
        计算调整后的级别
        
        Returns:
            (调整后级别, 调整类型, 原因列表)
        """
        base_level = context.get_effective_level()
        base_strictness = get_level_strictness(base_level.value)
        
        # 收集升级和降级
        upgrades = []
        downgrades = []
        
        for rule in rules:
            if rule.action == "UPGRADE":
                if rule.target_level:
                    target_strictness = get_level_strictness(rule.target_level.value)
                    upgrades.append((rule, target_strictness, rule.target_level))
                else:
                    # 按 delta 计算
                    new_strictness = min(base_strictness + rule.level_delta, 6)
                    target_level = self._strictness_to_level(new_strictness)
                    upgrades.append((rule, new_strictness, target_level))
                    
            elif rule.action == "DOWNGRADE":
                if rule.target_level:
                    target_strictness = get_level_strictness(rule.target_level.value)
                    downgrades.append((rule, target_strictness, rule.target_level))
                else:
                    # 按 delta 计算
                    new_strictness = max(base_strictness - rule.level_delta, 1)
                    target_level = self._strictness_to_level(new_strictness)
                    downgrades.append((rule, new_strictness, target_level))
        
        # 决策逻辑：升级优先于降级（安全第一）
        if upgrades:
            # 选择最严格的升级
            best_upgrade = max(upgrades, key=lambda x: x[1])
            rule, strictness, level = best_upgrade
            reason = f"{rule.name}: {base_level.value} -> {level.value}"
            return level, "UPGRADE", [reason]
        
        if downgrades:
            # 选择最宽松的降级（但不超过原始级别）
            best_downgrade = min(downgrades, key=lambda x: x[1])
            rule, strictness, level = best_downgrade
            reason = f"{rule.name}: {base_level.value} -> {level.value}"
            return level, "DOWNGRADE", [reason]
        
        # 无调整
        return base_level, "UNCHANGED", []
    
    def _strictness_to_level(self, strictness: int) -> DataLevel:
        """严格度数值转级别"""
        mapping = {
            1: DataLevel.L1_PUBLIC,
            2: DataLevel.L2_INTERNAL,
            3: DataLevel.L3_RESTRICTED,
            4: DataLevel.L4_CONFIDENTIAL,
            5: DataLevel.L5_SECRET,
            6: DataLevel.L6_CRITICAL
        }
        return mapping.get(strictness, DataLevel.L3_RESTRICTED)
    
    # ========== 便捷方法 ==========
    
    def check_aggregation_upgrade(
        self,
        base_level: DataLevel,
        record_count: int,
        aggregation_type: AggregationType
    ) -> Optional[DataLevel]:
        """
        检查是否需要汇聚升级
        
        Args:
            base_level: 基础级别
            record_count: 记录数量
            aggregation_type: 汇聚类型
            
        Returns:
            升级后的级别，或 None（无需升级）
        """
        for threshold in self.aggregation_thresholds:
            if (threshold.base_level == base_level and
                threshold.aggregation_type == aggregation_type and
                record_count >= threshold.threshold_count):
                return threshold.target_level
        
        return None
    
    def check_desensitization_downgrade(
        self,
        base_level: DataLevel,
        desensitization_methods: List[DesensitizationMethod]
    ) -> Optional[DataLevel]:
        """
        检查脱敏后的降级
        
        规则：
        - L3 + 手机号/邮箱/身份证掩码 -> L2
        - L4 + 强脱敏（哈希/抑制） -> L3
        
        Args:
            base_level: 原始级别
            desensitization_methods: 应用的脱敏方法
            
        Returns:
            降级后的级别，或 None
        """
        if not desensitization_methods:
            return None
        
        # L3 数据脱敏降级规则
        if base_level == DataLevel.L3_RESTRICTED:
            if any(m in desensitization_methods for m in [
                DesensitizationMethod.MASK_PHONE,
                DesensitizationMethod.MASK_EMAIL,
                DesensitizationMethod.MASK_IDCARD
            ]):
                return DataLevel.L2_INTERNAL
        
        # L4 数据强脱敏降级规则
        if base_level == DataLevel.L4_CONFIDENTIAL:
            if any(m in desensitization_methods for m in [
                DesensitizationMethod.HASH,
                DesensitizationMethod.SUPPRESSION,
                DesensitizationMethod.GENERALIZATION
            ]):
                return DataLevel.L3_RESTRICTED
        
        return None
    
    def check_time_decay_downgrade(
        self,
        base_level: DataLevel,
        data_created_at: datetime,
        has_incident: bool = False
    ) -> Optional[DataLevel]:
        """
        检查时间衰减降级
        
        Args:
            base_level: 基础级别
            data_created_at: 数据创建时间
            has_incident: 是否发生过安全事件
            
        Returns:
            降级后的级别，或 None
        """
        policy = self.time_decay_policies.get(base_level)
        if not policy:
            return None
        
        # 检查衰减条件
        if policy.require_no_incident and has_incident:
            return None
        
        # 计算天数
        days_passed = (datetime.now() - data_created_at).days
        
        # 查找适用的降级目标
        for threshold_days, target_level in sorted(policy.decay_schedule, reverse=True):
            if days_passed >= threshold_days:
                return target_level
        
        return None
    
    def calculate_aggregation_risk_score(
        self,
        classifications: List[ClassificationResult],
        aggregation_type: AggregationType
    ) -> float:
        """
        计算汇聚风险评分
        
        评分因素：
        - 高敏感数据占比
        - 数据总量
        - 汇聚类型风险
        
        Returns:
            风险评分 (0-1)
        """
        if not classifications:
            return 0.0
        
        # 计算高敏感数据占比
        high_sensitivity_count = sum(
            1 for c in classifications
            if get_level_strictness(c.level) >= 4  # L4+
        )
        high_sensitivity_ratio = high_sensitivity_count / len(classifications)
        
        # 汇聚类型风险系数
        type_risk = {
            AggregationType.BULK_EXPORT: 0.8,
            AggregationType.DATA_JOIN: 0.9,
            AggregationType.BATCH_QUERY: 0.5,
            AggregationType.STATISTICAL_ANALYSIS: 0.3
        }.get(aggregation_type, 0.5)
        
        # 总量风险系数（对数增长）
        import math
        volume_risk = min(math.log10(len(classifications)) / 3, 1.0)
        
        # 综合评分
        risk_score = (
            high_sensitivity_ratio * 0.4 +
            type_risk * 0.3 +
            volume_risk * 0.3
        )
        
        return min(risk_score, 1.0)
    
    # ========== 规则管理 ==========
    
    def add_rule(self, rule: DynamicRule) -> None:
        """添加动态规则"""
        self.rules.append(rule)
        logger.info(f"添加动态规则: {rule.id}")
    
    def remove_rule(self, rule_id: str) -> bool:
        """移除动态规则"""
        for i, rule in enumerate(self.rules):
            if rule.id == rule_id:
                self.rules.pop(i)
                logger.info(f"移除动态规则: {rule_id}")
                return True
        return False
    
    def enable_rule(self, rule_id: str) -> bool:
        """启用规则"""
        for rule in self.rules:
            if rule.id == rule_id:
                rule.enabled = True
                return True
        return False
    
    def disable_rule(self, rule_id: str) -> bool:
        """禁用规则"""
        for rule in self.rules:
            if rule.id == rule_id:
                rule.enabled = False
                return True
        return False
    
    def list_rules(self) -> List[Dict[str, Any]]:
        """列出所有规则"""
        return [
            {
                "id": r.id,
                "name": r.name,
                "type": r.rule_type.value,
                "action": r.action,
                "enabled": r.enabled,
                "priority": r.priority
            }
            for r in self.rules
        ]
    
    # ========== 上下文构建器 ==========
    
    def build_aggregation_context(
        self,
        base_result: ClassificationResult,
        record_count: int,
        aggregation_type: AggregationType,
        **kwargs
    ) -> DynamicClassificationContext:
        """构建汇聚场景上下文"""
        return DynamicClassificationContext(
            base_classification=base_result,
            record_count=record_count,
            aggregation_type=aggregation_type,
            **kwargs
        )
    
    def build_desensitization_context(
        self,
        base_result: ClassificationResult,
        desensitization_methods: List[DesensitizationMethod],
        **kwargs
    ) -> DynamicClassificationContext:
        """构建脱敏场景上下文"""
        return DynamicClassificationContext(
            base_classification=base_result,
            is_desensitized=True,
            desensitization_methods=desensitization_methods,
            original_level=DataLevel(base_result.level) if base_result.level else None,
            **kwargs
        )
    
    def build_correlation_context(
        self,
        base_result: ClassificationResult,
        correlated_fields: List[str],
        correlation_score: float,
        can_identify_individual: bool,
        **kwargs
    ) -> DynamicClassificationContext:
        """构建关联场景上下文"""
        return DynamicClassificationContext(
            base_classification=base_result,
            correlated_fields=correlated_fields,
            correlation_score=correlation_score,
            can_identify_individual=can_identify_individual,
            **kwargs
        )


# ========== 集成适配器 ==========

class DynamicClassificationAdapter:
    """
    动态分级与静态规则引擎的集成适配器
    
    提供统一的分级接口，自动应用动态规则
    """
    
    def __init__(
        self,
        static_engine: Any,  # ClassificationEngine
        dynamic_engine: Optional[DynamicClassificationEngine] = None
    ):
        self.static_engine = static_engine
        self.dynamic_engine = dynamic_engine or DynamicClassificationEngine()
    
    async def classify(
        self,
        path: str,
        apply_dynamic: bool = True,
        dynamic_context: Optional[DynamicClassificationContext] = None
    ) -> ClassificationResult:
        """
        统一分级接口
        
        Args:
            path: 文件路径
            apply_dynamic: 是否应用动态分级
            dynamic_context: 动态分级上下文（可选）
            
        Returns:
            最终分级结果
        """
        # 1. 静态分级
        base_result = await self.static_engine.classify(path)
        
        # 2. 如果不应用动态分级，直接返回
        if not apply_dynamic:
            return base_result
        
        # 3. 构建默认上下文（如果没有提供）
        if dynamic_context is None:
            dynamic_context = DynamicClassificationContext(
                base_classification=base_result,
                record_count=1
            )
        
        # 4. 应用动态分级
        dynamic_result = await self.dynamic_engine.classify_with_context(
            base_result, dynamic_context
        )
        
        # 5. 返回调整后的结果
        return dynamic_result.to_classification_result()
    
    async def classify_batch(
        self,
        paths: List[str],
        aggregation_type: AggregationType = AggregationType.BULK_EXPORT
    ) -> List[ClassificationResult]:
        """
        批量分级（自动应用汇聚升级规则）
        
        Args:
            paths: 文件路径列表
            aggregation_type: 汇聚类型
            
        Returns:
            分级结果列表
        """
        # 1. 静态分级所有路径
        base_results = []
        for path in paths:
            result = await self.static_engine.classify(path)
            base_results.append(result)
        
        # 2. 按级别分组
        from collections import defaultdict
        level_groups = defaultdict(list)
        for result in base_results:
            level_groups[result.level].append(result)
        
        # 3. 对每个分组应用动态分级
        final_results = []
        for level, results in level_groups.items():
            for result in results:
                context = DynamicClassificationContext(
                    base_classification=result,
                    record_count=len(results),
                    aggregation_type=aggregation_type
                )
                
                dynamic_result = await self.dynamic_engine.classify_with_context(
                    result, context
                )
                final_results.append(dynamic_result.to_classification_result())
        
        return final_results
