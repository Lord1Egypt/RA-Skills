"""
动态分级机制 - 数据模型

核心概念：
- 数据分级不是静态的，会随上下文变化
- 支持升级（汇聚、关联）和降级（脱敏、时间衰减）
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Callable, Any, Set
from enum import Enum
from pathlib import Path

from .models import DataLevel, ClassificationResult, get_level_strictness


class DynamicRuleType(Enum):
    """动态规则类型"""
    AGGREGATION_UPGRADE = "aggregation_upgrade"      # 数据汇聚升级
    DESENSITIZATION_DOWNGRADE = "desensitization_downgrade"  # 脱敏降级
    TIME_DECAY_DOWNGRADE = "time_decay_downgrade"    # 时间衰减降级
    CORRELATION_UPGRADE = "correlation_upgrade"      # 关联增强升级
    CONTEXT_UPGRADE = "context_upgrade"              # 上下文升级


class AggregationType(Enum):
    """汇聚类型"""
    BULK_EXPORT = "bulk_export"          # 批量导出
    BATCH_QUERY = "batch_query"          # 批量查询
    DATA_JOIN = "data_join"              # 数据关联
    STATISTICAL_ANALYSIS = "statistical_analysis"  # 统计分析


class DesensitizationMethod(Enum):
    """脱敏方法"""
    MASK_PHONE = "mask_phone"            # 手机号掩码 (138****1234)
    MASK_EMAIL = "mask_email"            # 邮箱掩码 (a***@example.com)
    MASK_IDCARD = "mask_idcard"          # 身份证掩码
    MASK_NAME = "mask_name"              # 姓名掩码 (张**)
    HASH = "hash"                        # 哈希化
    TRUNCATE = "truncate"                # 截断
    GENERALIZATION = "generalization"    # 泛化（如：具体地址→城市）
    SUPPRESSION = "suppression"          # 抑制（删除）


@dataclass
class DynamicClassificationContext:
    """
    动态分级上下文
    
    包含影响分级的动态因素
    """
    # 基础信息
    base_classification: ClassificationResult  # 基础分级结果
    
    # 汇聚信息
    record_count: int = 1                      # 记录数量
    aggregation_type: Optional[AggregationType] = None  # 汇聚类型
    
    # 脱敏信息
    is_desensitized: bool = False              # 是否已脱敏
    desensitization_methods: List[DesensitizationMethod] = field(default_factory=list)
    original_level: Optional[DataLevel] = None  # 原始级别（脱敏前）
    
    # 时间信息
    data_created_at: Optional[datetime] = None  # 数据创建时间
    data_modified_at: Optional[datetime] = None # 数据修改时间
    
    # 关联信息
    correlated_fields: List[str] = field(default_factory=list)  # 关联字段
    correlation_score: float = 0.0             # 关联强度（0-1）
    can_identify_individual: bool = False      # 是否能识别个人
    
    # 上下文信息
    user_role: Optional[str] = None            # 用户角色
    access_purpose: Optional[str] = None       # 访问目的
    destination: Optional[str] = None          # 数据去向
    
    # 元数据
    context_created_at: datetime = field(default_factory=datetime.now)
    context_source: str = "auto"               # 来源：auto/manual/system
    
    def get_effective_level(self) -> DataLevel:
        """获取当前有效级别（字符串转枚举）"""
        if isinstance(self.base_classification.level, str):
            return DataLevel(self.base_classification.level)
        return self.base_classification.level
    
    def get_strictness(self) -> int:
        """获取当前严格度"""
        return get_level_strictness(self.base_classification.level)


@dataclass
class DynamicRule:
    """
    动态分级规则
    
    定义在什么条件下如何调整数据级别
    """
    # 规则标识
    id: str
    name: str
    rule_type: DynamicRuleType
    
    # 触发条件（函数类型，必须提供）
    condition: Callable[[DynamicClassificationContext], bool] = field(repr=False)
    
    # 执行动作
    action: str  # 'UPGRADE' | 'DOWNGRADE' | 'MAINTAIN'
    
    # 目标级别（可选，如果为空则按规则逻辑计算）
    target_level: Optional[DataLevel] = None
    
    # 级别调整步数（1=升/降一级，2=升/降两级）
    level_delta: int = 1
    
    # 适用级别范围（哪些级别可以触发此规则）
    applicable_levels: List[DataLevel] = field(default_factory=list)
    
    # 描述
    description: str = ""
    
    # 优先级（数字越小优先级越高）
    priority: int = 100
    
    # 是否启用
    enabled: bool = True
    
    # 审计信息
    created_at: datetime = field(default_factory=datetime.now)
    created_by: str = "system"
    
    def applies_to(self, context: DynamicClassificationContext) -> bool:
        """检查规则是否适用于给定上下文"""
        if not self.enabled:
            return False
        
        # 检查级别范围
        if self.applicable_levels:
            if context.get_effective_level() not in self.applicable_levels:
                return False
        
        # 检查条件
        try:
            return self.condition(context)
        except Exception as e:
            # 条件评估失败，不应用此规则
            return False


@dataclass
class DynamicClassificationResult:
    """
    动态分级结果
    
    包含分级调整详情，用于审计和追溯
    """
    # 分级信息（非默认）
    original_result: ClassificationResult      # 原始分级结果
    adjusted_level: DataLevel                  # 调整后的级别
    
    # 调整详情（非默认）
    adjustment_type: str                       # 'UPGRADE' | 'DOWNGRADE' | 'UNCHANGED'
    adjustment_reason: str                     # 调整原因说明
    
    # 上下文快照（非默认）
    context: DynamicClassificationContext      # 触发调整的上下文
    
    # 应用的规则（默认）
    applied_rules: List[str] = field(default_factory=list)  # 应用的规则ID
    
    # 审计信息（默认）
    adjusted_at: datetime = field(default_factory=datetime.now)
    adjusted_by: str = "system"                # 调整者
    
    # 元数据（默认）
    is_manual_override: bool = False           # 是否人工覆盖
    manual_override_reason: Optional[str] = None
    
    def to_classification_result(self) -> ClassificationResult:
        """转换为标准分级结果"""
        result = ClassificationResult(
            path=self.original_result.path,
            level=self.adjusted_level.value,
            rule_id=self.original_result.rule_id,
            source=f"dynamic_{self.adjustment_type.lower()}",
            confidence=self.original_result.confidence,
            reason=f"{self.original_result.reason} -> {self.adjustment_reason}",
            status=self.original_result.status,
            note=self._format_note()
        )
        return result
    
    def _format_note(self) -> str:
        """格式化备注信息"""
        notes = []
        if self.applied_rules:
            notes.append(f"规则: {', '.join(self.applied_rules)}")
        if self.is_manual_override:
            notes.append(f"人工覆盖: {self.manual_override_reason}")
        return "; ".join(notes)


@dataclass
class AggregationThreshold:
    """
    汇聚升级阈值配置
    
    定义不同级别、不同汇聚类型的升级阈值
    """
    # 基础级别
    base_level: DataLevel
    
    # 汇聚类型
    aggregation_type: AggregationType
    
    # 阈值配置
    threshold_count: int                       # 记录数量阈值
    
    # 升级目标
    target_level: DataLevel
    
    # 说明
    reason: str = ""
    
    # 百分比阈值（可选）
    threshold_percentage: Optional[float] = None  # 百分比阈值（相对于总量）


@dataclass
class TimeDecayPolicy:
    """
    时间衰减策略
    
    定义数据随时间的级别衰减规则
    """
    # 适用级别
    applicable_level: DataLevel
    
    # 衰减时间线
    decay_schedule: List[tuple] = field(default_factory=list)
    # 示例: [(30, L3), (90, L2), (365, L1)] 表示30天后降为L3，90天后L2，365天后L1
    
    # 衰减条件
    require_access_history: bool = False       # 是否需要访问历史
    require_no_incident: bool = True           # 是否要求无安全事件
    
    def get_level_after_days(self, days: int) -> Optional[DataLevel]:
        """获取指定天数后的级别"""
        for threshold_days, target_level in sorted(self.decay_schedule, reverse=True):
            if days >= threshold_days:
                return target_level
        return None


# ========== 预设规则 ==========

def create_default_dynamic_rules() -> List[DynamicRule]:
    """创建默认动态分级规则"""
    
    return [
        # 规则1: L2数据批量汇聚升级
        DynamicRule(
            id="agg_l2_to_l3",
            name="L2批量汇聚升级",
            rule_type=DynamicRuleType.AGGREGATION_UPGRADE,
            condition=lambda ctx: (
                ctx.get_effective_level() == DataLevel.L2_INTERNAL and
                ctx.record_count >= 100 and
                ctx.aggregation_type in [AggregationType.BULK_EXPORT, AggregationType.BATCH_QUERY]
            ),
            action="UPGRADE",
            target_level=DataLevel.L3_RESTRICTED,
            applicable_levels=[DataLevel.L2_INTERNAL],
            description="L2内部数据，当批量汇聚超过100条时升级为L3",
            priority=10
        ),
        
        # 规则2: L3数据批量汇聚升级
        DynamicRule(
            id="agg_l3_to_l4",
            name="L3批量汇聚升级",
            rule_type=DynamicRuleType.AGGREGATION_UPGRADE,
            condition=lambda ctx: (
                ctx.get_effective_level() == DataLevel.L3_RESTRICTED and
                ctx.record_count >= 50 and
                ctx.aggregation_type in [AggregationType.BULK_EXPORT, AggregationType.DATA_JOIN]
            ),
            action="UPGRADE",
            target_level=DataLevel.L4_CONFIDENTIAL,
            applicable_levels=[DataLevel.L3_RESTRICTED],
            description="L3受限数据，当批量汇聚超过50条时升级为L4",
            priority=10
        ),
        
        # 规则3: 手机号脱敏降级
        DynamicRule(
            id="desens_phone_l3_to_l2",
            name="手机号脱敏降级",
            rule_type=DynamicRuleType.DESENSITIZATION_DOWNGRADE,
            condition=lambda ctx: (
                ctx.get_effective_level() == DataLevel.L3_RESTRICTED and
                ctx.is_desensitized and
                DesensitizationMethod.MASK_PHONE in ctx.desensitization_methods
            ),
            action="DOWNGRADE",
            target_level=DataLevel.L2_INTERNAL,
            applicable_levels=[DataLevel.L3_RESTRICTED],
            description="L3手机号数据，脱敏后可降级为L2",
            priority=20
        ),
        
        # 规则4: 强关联识别个人升级
        DynamicRule(
            id="correlation_identify_upgrade",
            name="关联识别个人升级",
            rule_type=DynamicRuleType.CORRELATION_UPGRADE,
            condition=lambda ctx: (
                ctx.can_identify_individual and
                ctx.correlation_score > 0.8 and
                ctx.get_effective_level().value < DataLevel.L4_CONFIDENTIAL.value
            ),
            action="UPGRADE",
            level_delta=1,  # 升一级
            applicable_levels=[
                DataLevel.L1_PUBLIC,
                DataLevel.L2_INTERNAL,
                DataLevel.L3_RESTRICTED
            ],
            description="当多条数据关联后可识别个人身份时升级",
            priority=5  # 高优先级
        ),
        
        # 规则5: 跨域传输升级
        DynamicRule(
            id="cross_domain_upgrade",
            name="跨域传输升级",
            rule_type=DynamicRuleType.CONTEXT_UPGRADE,
            condition=lambda ctx: (
                ctx.destination is not None and
                ctx.destination.startswith("external_") and
                ctx.get_effective_level().value < DataLevel.L5_SECRET.value
            ),
            action="UPGRADE",
            level_delta=1,
            applicable_levels=[
                DataLevel.L1_PUBLIC,
                DataLevel.L2_INTERNAL,
                DataLevel.L3_RESTRICTED,
                DataLevel.L4_CONFIDENTIAL
            ],
            description="数据跨域传输时自动升一级",
            priority=15
        ),
    ]


def create_default_aggregation_thresholds() -> List[AggregationThreshold]:
    """创建默认汇聚升级阈值"""
    return [
        # L2 数据批量导出阈值
        AggregationThreshold(
            base_level=DataLevel.L2_INTERNAL,
            aggregation_type=AggregationType.BULK_EXPORT,
            threshold_count=100,
            target_level=DataLevel.L3_RESTRICTED,
            reason="L2数据批量导出超过100条，风险增加"
        ),
        
        # L3 数据批量导出阈值
        AggregationThreshold(
            base_level=DataLevel.L3_RESTRICTED,
            aggregation_type=AggregationType.BULK_EXPORT,
            threshold_count=50,
            target_level=DataLevel.L4_CONFIDENTIAL,
            reason="L3数据批量导出超过50条，风险增加"
        ),
        
        # L3 数据关联阈值（关联后可能识别个人）
        AggregationThreshold(
            base_level=DataLevel.L3_RESTRICTED,
            aggregation_type=AggregationType.DATA_JOIN,
            threshold_count=10,
            target_level=DataLevel.L4_CONFIDENTIAL,
            reason="L3数据关联超过10条，可能识别个人身份"
        ),
    ]


def create_default_time_decay_policies() -> List[TimeDecayPolicy]:
    """创建默认时间衰减策略"""
    return [
        # L3 受限数据衰减策略
        TimeDecayPolicy(
            applicable_level=DataLevel.L3_RESTRICTED,
            decay_schedule=[
                (90, DataLevel.L2_INTERNAL),    # 90天后降为L2
                (365, DataLevel.L1_PUBLIC),     # 1年后降为L1
            ],
            require_no_incident=True
        ),
        
        # L4 机密数据衰减策略
        TimeDecayPolicy(
            applicable_level=DataLevel.L4_CONFIDENTIAL,
            decay_schedule=[
                (180, DataLevel.L3_RESTRICTED),  # 180天后降为L3
                (730, DataLevel.L2_INTERNAL),    # 2年后降为L2
            ],
            require_no_incident=True
        ),
    ]
