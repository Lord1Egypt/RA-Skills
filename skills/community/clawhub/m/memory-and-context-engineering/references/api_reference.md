# API 参考文档

本文档提供 Agent Memory System 的完整 API 参考。

> **架构说明**：Agent Memory System 采用**四层架构**：
> - **顶层：总控层** - ContextOrchestrator（统一入口、全局调度）
> - **中间层：协调层** - 认知模型层（核心业务逻辑）+ 双轨架构（技术实现）
> - **基础层：存储层** - 短期/长期记忆、索引管理
> - **底层：基础设施层** - 类型定义、加密隐私、监控优化
>
> 详见 [架构总览](architecture_overview.md)。

## 目录

1. [顶层：总控层 - ContextOrchestrator](#顶层总控层-contextorchestrator)
2. [PriorityResolver](#priorityresolver)
3. [MetadataQualityAssessor](#metadataqualityassessor)
4. [CustomTypeLifecycleManager](#customtypelifecyclemanager)
5. [UsageMonitor](#usagemonitor)
6. [LRUCache](#lrucache)
7. [PerformanceMonitor](#performancemonitor)
8. [BatchProcessor](#batchprocessor)
9. [协调层：双轨架构 API](#协调层双轨架构-api)
10. [链感知上下文压缩 API](#链感知上下文压缩-api)

---

## 顶层：总控层 - ContextOrchestrator

ContextOrchestrator 是系统的**统一入口和总控中心**（顶层），负责：
- Token 预算管理
- 检索决策
- 多源协调（认知模型、双轨、存储层）
- 结果压缩
- 全局调度
- 可观测性管理

### 层级关系

```
ContextOrchestrator (总控层)
    │
    ├─→ 认知模型层（协调层子层）
    │   ├─ CognitiveModelBuilder
    │   ├─ CausalChainExtractor
    │   └─ ...（其他7个组件）
    │
    ├─→ 双轨架构（协调层子层）
    │   ├─ 轨道A：语义桶提炼
    │   ├─ 轨道B：链提取
    │   └─ 融合层
    │
    ├─→ 存储层（基础层）
    │   ├─ ShortTermMemoryManager
    │   └─ LongTermMemoryManager
    │
    └─→ 基础设施层（底层）
        ├─ type_defs
        ├─ encryption
        └─ monitoring
```

### 初始化

```python
from scripts.redis_adapter import create_redis_adapter
from scripts.context_orchestrator import ContextOrchestrator

redis_adapter = create_redis_adapter(host="localhost", port=6379)
orchestrator = ContextOrchestrator(
    redis_adapter=redis_adapter,
    user_id="user123",
    session_id="session456",
)
```

### 方法

#### prepare_context()

准备完整上下文。

```python
def prepare_context(
    self,
    user_input: str,
    system_instruction: str | None = None,
    retrieval_results: list[str] | None = None,
    tool_results: list[str] | None = None,
    additional_blocks: list[ContextBlock] | None = None,
) -> PreparedContext
```

**参数**：
- `user_input` (str): 用户输入
- `system_instruction` (str | None): 系统指令
- `retrieval_results` (list[str] | None): 检索结果列表
- `tool_results` (list[str] | None): 工具返回列表
- `additional_blocks` (list[ContextBlock] | None): 额外的上下文块

**返回值**：`PreparedContext` - 准备好的上下文

#### register_custom_type()

注册自定义类型。

```python
def register_custom_type(
    self,
    custom_type: str,
    priority: ContextPriority,
    required_fields: list[str] = None,
) -> None
```

**参数**：
- `custom_type` (str): 自定义类型名称
- `priority` (ContextPriority): 优先级
- `required_fields` (list[str] | None): 必需字段列表

#### enable_quality_assessment()

启用质量评估与生命周期管理。

```python
def enable_quality_assessment(
    self,
    storage_path: str = "usage_stats.json",
    enable_monitoring: bool = False,
) -> None
```

**参数**：
- `storage_path` (str): 统计数据存储路径
- `enable_monitoring` (bool): 是否启用使用监控

#### enable_performance_monitoring()

启用性能监控。

```python
def enable_performance_monitoring(self) -> None
```

#### get_performance_stats()

获取性能统计。

```python
def get_performance_stats(self) -> dict[str, Any] | None
```

**返回值**：性能统计字典

---

## PriorityResolver

优先级解析器，根据 source 和 metadata 解析最终的优先级。

### 初始化

```python
from scripts.context_orchestrator import PriorityResolver

resolver = PriorityResolver(enable_lru_cache=True, cache_size=1000)
```

### 方法

#### resolve()

解析优先级。

```python
def resolve(
    self,
    source: ContextSource,
    metadata: dict[str, Any]
) -> tuple[ContextPriority, str]
```

**参数**：
- `source` (ContextSource): 上下文来源
- `metadata` (dict[str, Any]): metadata 字典

**返回值**：(优先级, 解析日志)

#### register_custom_type()

注册自定义类型。

```python
def register_custom_type(
    self,
    custom_type: str,
    priority: ContextPriority,
    required_fields: list[str] = None,
) -> None
```

#### get_cache_stats()

获取缓存统计。

```python
def get_cache_stats(self) -> dict[str, Any]
```

**返回值**：缓存统计字典

---

## MetadataQualityAssessor

质量评估器，评估 metadata 的完整性、准确性、一致性和实用性。

### 初始化

```python
from scripts.context_orchestrator import MetadataQualityAssessor

assessor = MetadataQualityAssessor(
    weights={
        "completeness": 0.4,
        "accuracy": 0.3,
        "consistency": 0.2,
        "usability": 0.1,
    }
)
```

### 方法

#### assess_quality()

评估 metadata 质量。

```python
def assess_quality(
    self,
    metadata: dict[str, Any],
    source: ContextSource,
    custom_types_registry: dict[str, dict]
) -> QualityAssessment
```

**参数**：
- `metadata` (dict[str, Any]): metadata 字典
- `source` (ContextSource): 上下文来源
- `custom_types_registry` (dict[str, dict]): 自定义类型注册表

**返回值**：`QualityAssessment` - 质量评估结果

---

## CustomTypeLifecycleManager

自定义类型生命周期管理器，管理自定义类型的创建、使用、废弃和清理。

### 初始化

```python
from scripts.context_orchestrator import CustomTypeLifecycleManager

manager = CustomTypeLifecycleManager(storage_path="usage_stats.json")
```

### 方法

#### register_type()

注册自定义类型。

```python
def register_type(
    self,
    custom_type: str,
    priority: ContextPriority,
    required_fields: list[str] | None = None,
    description: str = "",
    creator: str = "unknown",
) -> None
```

#### track_usage()

记录类型使用。

```python
def track_usage(
    self,
    custom_type: str,
    usage_info: dict[str, Any] | None = None,
) -> None
```

#### deprecate_type()

废弃类型。

```python
def deprecate_type(
    self,
    custom_type: str,
    reason: str = "",
) -> None
```

#### cleanup_unused_types()

清理长期未使用的类型。

```python
def cleanup_unused_types(self, threshold_days: int = 90) -> list[str]
```

**返回值**：被清理的类型列表

---

## UsageMonitor

使用情况监控器，监控 metadata 的使用情况。

### 初始化

```python
from scripts.context_orchestrator import UsageMonitor

monitor = UsageMonitor()
```

### 方法

#### record_usage()

记录使用。

```python
def record_usage(
    self,
    source: ContextSource,
    subtype: str | None = None,
    custom_type: str | None = None,
    metadata_fields: list[str] | None = None,
) -> None
```

#### get_usage_stats()

获取使用统计。

```python
def get_usage_stats(self) -> dict[str, Any]
```

#### generate_usage_report()

生成使用报告。

```python
def generate_usage_report(self) -> str
```

---

## LRUCache

LRU（最近最少使用）缓存实现。

### 初始化

```python
from scripts.context_orchestrator import LRUCache

cache = LRUCache(max_size=1000)
```

### 方法

#### get()

获取缓存值。

```python
def get(self, key: str) -> Any | None
```

#### put()

设置缓存值。

```python
def put(self, key: str, value: Any) -> None
```

#### clear()

清空缓存。

```python
def clear(self) -> None
```

#### stats()

获取缓存统计。

```python
def stats(self) -> dict[str, Any]
```

---

## PerformanceMonitor

性能监控器，监控操作延迟、吞吐量和资源使用。

### 初始化

```python
from scripts.context_orchestrator import PerformanceMonitor

monitor = PerformanceMonitor()
```

### 方法

#### record_operation()

记录操作时间。

```python
def record_operation(
    self,
    operation_name: str,
    duration: float,
) -> None
```

#### get_stats()

获取性能统计。

```python
def get_stats(self) -> dict[str, Any]
```

#### generate_report()

生成性能报告。

```python
def generate_report(self) -> str
```

---

## BatchProcessor

批量处理器，优化批量处理操作的性能。

### 静态方法

#### validate_metadata_batch()

批量验证 metadata。

```python
@staticmethod
def validate_metadata_batch(
    metadata_list: list[dict[str, Any]],
    source_list: list[ContextSource]
) -> list[ValidationResult]
```

#### resolve_priorities_batch_optimized()

优化的批量优先级解析。

```python
@staticmethod
def resolve_priorities_batch_optimized(
    resolver: PriorityResolver,
    blocks: list[ContextBlock]
) -> list[tuple[ContextPriority, str]]
```

#### assess_quality_batch()

批量质量评估。

```python
@staticmethod
def assess_quality_batch(
    assessor: MetadataQualityAssessor,
    blocks: list[ContextBlock],
    custom_types_registry: dict[str, dict],
) -> list[QualityAssessment]
```

---

## 数据模型

### ContextBlock

上下文块数据模型。

```python
class ContextBlock(BaseModel):
    source: ContextSource                    # 来源
    priority: ContextPriority                # 优先级
    content: str                             # 内容
    token_count: int                         # Token 数量
    metadata: dict[str, Any]                 # 元数据
    relevance_score: float                   # 相关性分数
    freshness_score: float                   # 新鲜度分数
```

### QualityAssessment

质量评估结果数据模型。

```python
class QualityAssessment(BaseModel):
    score: float                             # 总分 (0-100)
    completeness_score: float                # 完整性得分
    accuracy_score: float                    # 准确性得分
    consistency_score: float                 # 一致性得分
    usability_score: float                   # 实用性得分
    issues: list[str]                        # 问题列表
    recommendations: list[str]               # 改进建议
```

### PreparedContext

准备好的上下文数据模型。

```python
class PreparedContext(BaseModel):
    content: str                             # 完整上下文内容
    token_count: int                         # 总 Token 数
    blocks: list[ContextBlock]               # 上下文块列表
    stats: dict[str, Any]                    # 统计信息
    warnings: list[str]                      # 警告信息
```

---

## 上下文压缩 API

### ContextCompressor

上下文压缩器，提供多种压缩策略。

#### enable_context_compression()

启用上下文压缩。

```python
def enable_context_compression(
    self,
    enable_auto_compress: bool = True,
    auto_compress_threshold: float = 0.8,
    default_strategy: str = "priority_based"
) -> None
```

**参数**：
- `enable_auto_compress` (bool): 是否启用自动压缩
- `auto_compress_threshold` (float): 自动压缩触发阈值（0.0-1.0）
- `default_strategy` (str): 默认压缩策略

#### compress_context()

手动压缩上下文。

```python
def compress_context(
    self,
    blocks: list[ContextBlock],
    compression_ratio: float = 0.7,
    min_blocks: int = 1,
    target_tokens: int | None = None,
    strategy: str = "priority_based"
) -> CompressionResult
```

**参数**：
- `blocks` (list[ContextBlock]): 上下文块列表
- `compression_ratio` (float): 压缩比率（保留的 token 比例）
- `min_blocks` (int): 最小保留块数
- `target_tokens` (int | None): 目标 token 数
- `strategy` (str): 压缩策略

**返回值**：`CompressionResult` - 压缩结果

**压缩策略**：
- `priority_based`: 基于优先级
- `relevance_based`: 基于相关性
- `freshness_based`: 基于新鲜度
- `composite`: 综合评分
- `rule_based`: 基于规则

### CompressionResult

压缩结果数据模型。

```python
class CompressionResult(BaseModel):
    compressed_blocks: list[ContextBlock]     # 压缩后的上下文块
    original_token_count: int                 # 原始 token 数
    compressed_token_count: int               # 压缩后 token 数
    compression_ratio: float                  # 压缩率
    removed_blocks: int                       # 移除的块数
    quality_score: float                      # 质量评分 (0-100)
    compression_time: float                   # 压缩时间（秒）
```

---

## 质量评估与监控 API

### MetadataQualityAssessor

Metadata 质量评估器，评估 metadata 的完整性、准确性、一致性和实用性。

#### assess_metadata_quality()

评估 metadata 质量。

```python
def assess_metadata_quality(
    self,
    metadata: dict[str, Any],
    source: ContextSource
) -> QualityAssessment
```

**参数**：
- `metadata` (dict[str, Any]): metadata 字典
- `source` (ContextSource): 上下文来源

**返回值**：`QualityAssessment` - 质量评估结果

#### generate_improvement_recommendations()

生成改进建议。

```python
def generate_improvement_recommendations(
    self,
    usage_stats: dict[str, Any]
) -> list[str]
```

**返回值**：改进建议列表

### CustomTypeLifecycleManager

自定义类型生命周期管理器。

#### register_custom_type()

注册自定义类型。

```python
def register_custom_type(
    self,
    custom_type: str,
    priority: ContextPriority,
    required_fields: list[str] = None,
    description: str = "",
    creator: str = "system"
) -> None
```

**参数**：
- `custom_type` (str): 自定义类型名称
- `priority` (ContextPriority): 优先级
- `required_fields` (list[str] | None): 必需字段列表
- `description` (str): 描述
- `creator` (str): 创建者

#### track_usage()

追踪使用情况。

```python
def track_usage(
    self,
    custom_type: str,
    usage_info: dict[str, Any]
) -> None
```

#### deprecate_type()

废弃类型。

```python
def deprecate_type(
    self,
    custom_type: str,
    reason: str = ""
) -> None
```

#### cleanup_unused_types()

清理未使用的类型。

```python
def cleanup_unused_types(
    self,
    threshold_days: int = 90
) -> list[str]
```

**返回值**：被清理的类型列表

### UsageMonitor

使用监控器，统计 metadata 使用情况。

#### record_metadata_usage()

记录 metadata 使用。

```python
def record_metadata_usage(
    self,
    source: ContextSource,
    subtype: str | None = None,
    custom_type: str | None = None,
    metadata_fields: list[str] = None
) -> None
```

#### get_usage_stats()

获取使用统计。

```python
def get_usage_stats(self) -> dict[str, Any]
```

**返回值**：使用统计字典

---

## 协调层：双轨架构 API

双轨架构是**协调层的子层**，为认知模型层提供结构化信息提取能力。

**层级定位**：
- 认知模型层（协调层核心）→ 定义"需要什么信息"
- 双轨架构（协调层子层）→ 实现"如何提取这些信息"

**双轨组成**：
- **轨道A：语义桶提炼** - 提取"是什么"（语义分类信息）
- **轨道B：链提取** - 提取"为什么"和"怎么"（结构化链信息）
- **融合层** - 关联、验证、摘要

**链类型（5种）**：
- **CAUSAL**（因果链）：问题→原因→解决方案
- **LOGIC**（逻辑链）：前提→推理→结论
- **OPERATION**（操作链）：动作→步骤→结果
- **NARRATIVE**（叙事链）：开端→发展→转折→结局
- **TIME**（时间链）：过去→现在→未来

详见 [双轨架构总览](dual_track_architecture_overview.md)。

### 链提取 API

#### BaseExtractedChain

链基类，定义所有链类型的统一接口。

```python
class BaseExtractedChain(BaseModel):
    chain_id: str                    # 链唯一标识
    chain_type: ChainType            # 链类型（CAUSAL, LOGIC, OPERATION, NARRATIVE, TIME）
    content: str                     # 链内容摘要
    extraction_confidence: float     # 提取置信度（0.0-1.0）
    extraction_timestamp: datetime   # 提取时间戳
```

#### ChainType

链类型枚举。

```python
class ChainType(str, Enum):
    CAUSAL = "causal"        # 因果链（问题-原因-解决方案）
    LOGIC = "logic"          # 逻辑链（前提-推理-结论）
    OPERATION = "operation"  # 操作链（步骤-结果）
    NARRATIVE = "narrative"  # 叙事链（事件序列）
    TIME = "time"            # 时间链（时间线）
```

#### ExtractedCausalChain

因果链实现，表示问题-原因-解决方案的结构。

```python
class ExtractedCausalChain(BaseExtractedChain):
    problem: ProblemNode        # 问题节点
    causes: list[CauseNode]     # 原因列表
    causal_relations: list[CausalRelation]  # 因果关系
    solutions: list[SolutionNode]  # 解决方案列表
```

**使用示例**：
```python
from scripts.chains.causal_chain import ExtractedCausalChain, ProblemNode, SolutionNode
from scripts.chains.base_chain import ChainType

chain = ExtractedCausalChain(
    chain_type=ChainType.CAUSAL,
    content="API错误导致数据库连接池耗尽",
    extraction_confidence=0.9,
    problem=ProblemNode(content="API 500错误"),
    solutions=[SolutionNode(content="增加连接池大小")]
)
```

### 链缓存管理 API

#### ChainCacheManager

链缓存管理器，使用LRU策略管理链缓存。

```python
class ChainCacheManager:
    def __init__(self, max_size: int = 1000, default_ttl: int = 300)
```

**参数**：
- `max_size` (int): 最大缓存容量
- `default_ttl` (int): 默认过期时间（秒）

#### put()

存储链到缓存。

```python
def put(
    self,
    chain_id: str,
    chain: BaseExtractedChain,
    chain_type: ChainType,
    ttl: int | None = None
) -> bool
```

**参数**：
- `chain_id` (str): 链ID
- `chain` (BaseExtractedChain): 链对象
- `chain_type` (ChainType): 链类型
- `ttl` (int | None): 过期时间（秒），None表示使用默认值

**返回值**：是否成功存储

**示例**：
```python
from scripts.processors.chain_cache_manager import ChainCacheManager
from scripts.chains.base_chain import ChainType

cache = ChainCacheManager(max_size=1000, default_ttl=60)
cache.put(
    chain_id=chain.chain_id,
    chain=chain,
    chain_type=ChainType.CAUSAL
)
```

#### get()

从缓存获取链。

```python
def get(self, chain_id: str) -> BaseExtractedChain | None
```

**参数**：
- `chain_id` (str): 链ID

**返回值**：链对象，如果不存在或已过期返回None

#### get_by_type()

按类型获取所有链。

```python
def get_by_type(self, chain_type: ChainType) -> list[BaseExtractedChain]
```

**参数**：
- `chain_type` (ChainType): 链类型

**返回值**：链列表

#### get_stats()

获取缓存统计信息。

```python
def get_stats(self) -> dict[str, Any]
```

**返回值**：统计信息字典（hits, misses, evictions, hit_rate, size）

### 监控系统 API

#### MonitoringSystem

监控系统，收集和报告双轨架构的监控指标。

```python
class MonitoringSystem:
    def __init__(self, max_metrics: int = 1000, monitoring_enabled: bool = True)
```

**参数**：
- `max_metrics` (int): 最大指标数量
- `monitoring_enabled` (bool): 是否启用监控

#### record_metric()

记录指标。

```python
def record_metric(
    self,
    name: str,
    value: float,
    labels: dict[str, str] | None = None
) -> None
```

**参数**：
- `name` (str): 指标名称
- `value` (float): 指标值
- `labels` (dict[str, str] | None): 标签

**示例**：
```python
from scripts.processors.monitoring_system import MonitoringSystem

monitor = MonitoringSystem()
monitor.record_metric("processing_time", 0.5, {"mode": "parallel"})
monitor.record_metric("cache_hit_rate", 0.8)
```

#### health_check()

记录健康检查结果。

```python
def health_check(
    self,
    component: str,
    status: str,
    message: str,
    details: dict | None = None
) -> None
```

**参数**：
- `component` (str): 组件名称
- `status` (str): 状态（healthy, degraded, unhealthy）
- `message` (str): 消息
- `details` (dict | None): 详情

#### get_overall_health()

获取整体健康状态。

```python
def get_overall_health(self) -> dict[str, Any]
```

**返回值**：整体健康状态字典

### 优化双轨处理器 API

#### OptimizedDualTrackProcessor

优化的双轨处理器，支持异步并行处理、缓存和性能监控。

```python
class OptimizedDualTrackProcessor:
    def __init__(
        self,
        enable_parallel: bool = True,
        enable_cache: bool = True,
        cache_ttl: int = 60
    )
```

**参数**：
- `enable_parallel` (bool): 是否启用并行处理
- `enable_cache` (bool): 是否启用缓存
- `cache_ttl` (int): 缓存TTL（秒）

#### process_input_async()

异步处理输入。

```python
async def process_input_async(
    self,
    text: str,
    context: dict[str, Any]
) -> ProcessingResult
```

**参数**：
- `text` (str): 输入文本
- `context` (dict[str, Any]): 上下文信息

**返回值**：ProcessingResult对象

**ProcessingResult结构**：
```python
class ProcessingResult:
    topic_clusters: list[Any]           # 话题簇列表
    extracted_chains: dict              # 提取的链字典
    bucket_chain_links: list[Any]       # 桶-链关联列表
    validation_results: list[Any]       # 验证结果列表
    extraction_action: Any              # 提取动作
    processing_time: float              # 处理时间（秒）
    performance_metrics: dict           # 性能指标
```

**示例**：
```python
import asyncio
from scripts.processors.optimized_dual_track_processor import OptimizedDualTrackProcessor

processor = OptimizedDualTrackProcessor()

async def process():
    result = await processor.process_input_async("用户输入文本", {})
    print(f"处理时间: {result.processing_time}")
    return result

result = asyncio.run(process())
```

#### get_performance_stats()

获取性能统计。

```python
def get_performance_stats(self) -> dict[str, Any]
```

**返回值**：性能统计字典（bucket_track_time, chain_track_time, fusion_time等）

### 集成适配器 API

#### DualTrackIntegrationAdapter

双轨集成适配器，提供与现有系统的集成接口。

```python
class DualTrackIntegrationAdapter:
    def __init__(
        self,
        processor: OptimizedDualTrackProcessor | None = None,
        cache_manager: ChainCacheManager | None = None,
        monitoring_system: MonitoringSystem | None = None,
        enable_health_check: bool = True
    )
```

#### process_message()

同步处理消息。

```python
def process_message(
    self,
    message: str,
    context: dict[str, Any] | None = None
) -> dict[str, Any]
```

**参数**：
- `message` (str): 消息内容
- `context` (dict[str, Any] | None): 上下文信息

**返回值**：处理结果字典

**返回值结构**：
```python
{
    "status": "success",           # 状态（success, error）
    "result": ProcessingResult,   # 处理结果
    "degraded_mode": bool,        # 是否降级模式
    "processing_time": float      # 处理时间（秒）
}
```

#### process_message_async()

异步处理消息。

```python
async def process_message_async(
    self,
    message: str,
    context: dict[str, Any] | None = None
) -> dict[str, Any]
```

**示例**：
```python
import asyncio
from scripts.processors.dual_track_integration_adapter import DualTrackIntegrationAdapter

adapter = DualTrackIntegrationAdapter()

async def process():
    result = await adapter.process_message_async("测试消息", {})
    print(f"状态: {result['status']}")
    return result

result = asyncio.run(process())
```

---

## 链感知上下文压缩 API

链感知压缩提供基于链信息的智能上下文压缩策略，优先保留包含5种链类型（因果、逻辑、操作、叙事、时间）的上下文块。

**与双轨架构的关系**：
- 双轨架构轨道B提取链信息
- 链感知压缩策略利用这些链信息进行智能压缩
- 形成完整的"提取→压缩"闭环

### ContextBlock 扩展

ContextBlock已扩展支持链元数据。

```python
class ContextBlock(BaseModel):
    # ... 原有字段 ...

    # 链元数据（链感知压缩支持）
    chain_links: list[str] = Field(default_factory=list, description="包含的链ID列表")
    chain_types: list[str] = Field(default_factory=list, description="包含的链类型列表")
```

**使用示例**：
```python
from scripts.context_orchestrator import ContextBlock, ContextSource, ContextPriority

block = ContextBlock(
    source=ContextSource.SHORT_TERM_MEMORY,
    priority=ContextPriority.HIGH,
    content="问题A→原因B→方案C",
    token_count=100,
    chain_links=["chain_001"],
    chain_types=["causal"]
)
```

### CHAIN_AWARE 压缩策略

#### CompressionStrategy.CHAIN_AWARE

链感知压缩策略，优先保留包含链信息的上下文块。

```python
class CompressionStrategy(str, Enum):
    # ... 其他策略 ...
    CHAIN_AWARE = "chain_aware"  # 链感知压缩
```

#### set_chain_type_weights()

设置链类型权重。

```python
def set_chain_type_weights(self, weights: dict[str, int]) -> None
```

**参数**：
- `weights` (dict[str, int]): 链类型到权重的映射

**默认权重**：
```python
{
    "causal": 40,      # 因果链
    "logic": 35,       # 逻辑链
    "operation": 35,   # 操作链
    "narrative": 30,   # 叙事链
    "time": 25         # 时间链
}
```

**示例**：
```python
from scripts.context_orchestrator import ContextCompressor, CompressionStrategy

compressor = ContextCompressor()

# 自定义权重
compressor.set_chain_type_weights({
    "causal": 50,    # 提高因果链权重
    "operation": 45  # 提高操作链权重
})

# 使用链感知压缩
result = compressor.compress(
    blocks=[block1, block2, ...],
    compression_ratio=0.5,
    strategy=CompressionStrategy.CHAIN_AWARE
)

print(f"压缩后保留链块数: {len([b for b in result.compressed_blocks if b.chain_links])}")
```

### 链感知评分公式

链感知压缩使用的评分公式：

```
链感知评分 = 基础优先级 + 链类型权重 + 链数量奖励 + 相关性 + 新鲜度

其中：
- 基础优先级：PRIORITY_WEIGHTS[priority] * 10
- 链类型权重：sum(WEIGHTS[type] for type in chain_types)
- 链数量奖励：len(chain_links) * 15
- 相关性：relevance_score * 10
- 新鲜度：freshness_score * 10
```

**示例计算**：
```
假设一个块：
- 优先级：HIGH (4.0)
- 链类型：["causal", "logic"]
- 链数量：2
- 相关性：0.8
- 新鲜度：0.9

评分 = 4.0 * 10 + (40 + 35) + 2 * 15 + 0.8 * 10 + 0.9 * 10
     = 40 + 75 + 30 + 8 + 9
     = 162
```

---

## API 快速参考

### 核心导入方式

```python
# 方式 1：导入工厂函数（推荐）
from scripts import create_context_orchestrator
from scripts import create_redis_adapter

# 方式 2：直接导入类
from scripts import ContextOrchestrator, SemanticBucketType
from scripts import PrivacyManager, ConsentStatus
```

### 四层架构快速参考

| 层级 | 核心模块 | 主要职责 | 关键API |
|------|---------|---------|---------|
| **顶层：总控层** | ContextOrchestrator | 统一入口、全局调度、Token预算、检索决策 | `prepare_context()`, `enable_context_compression()`, `compress_context()` |
| **中间层：协调层** | 认知模型层（9大组件） | 认知模型构建、因果链提取、知识缺口识别、检索决策等 | `CognitiveModelBuilder.build()`, `CausalChainExtractor.extract()` |
| **中间层：协调层** | 双轨架构（2轨道+融合层） | 语义桶提炼、链提取（5种）、融合层处理 | `OptimizedDualTrackProcessor.process()`, `ChainCacheManager.put()` |
| **基础层：存储层** | ShortTermMemory、LongTermMemory | 记忆持久化、索引管理、热度分层 | `store()`, `retrieve()`, `get_all_memories()` |
| **底层：基础设施层** | type_defs、encryption、monitoring | 类型定义、加密隐私、监控优化 | `encrypt()`, `decrypt()`, `record_metric()` |

### 双轨架构与认知模型层的关系

```
认知模型层（业务逻辑）← 双轨架构（技术实现）
    │                           │
    │ 需要什么信息？            │ 提供什么信息？
    │ - 任务上下文              │ - 语义桶（轨道A）
    │ - 因果关系                │ - 因果链（轨道B）
    │ - 逻辑推理                │ - 逻辑链（轨道B）
    │ - 操作步骤                │ - 操作链（轨道B）
    │ - 叙事线索                │ - 叙事链（轨道B）
    │ - 时间线索                │ - 时间链（轨道B）
```

### 常用 API 快速调用

| 功能 | 导入方式 | 快速调用示例 |
|------|----------|--------------|
| 上下文编排 | `from scripts import create_context_orchestrator` | `orchestrator = create_context_orchestrator(user_id="user123", session_id="session456")` |
| Redis 连接 | `from scripts import create_redis_adapter` | `redis_adapter = create_redis_adapter(host="localhost", port=6379)` |
| 隐私管理 | `from scripts import PrivacyManager, ConsentStatus` | `privacy_manager = PrivacyManager(user_id="user123")` |
| 感知记忆 | `from scripts import PerceptionMemoryStore` | `perception = PerceptionMemoryStore()` |
| 短期记忆 | `from scripts import ShortTermMemoryManager` | `short_term = ShortTermMemoryManager()` |
| 长期记忆 | `from scripts import LongTermMemoryManager` | `long_term = LongTermMemoryManager()` |
| 上下文重构 | `from scripts import ContextReconstructor` | `reconstructor = ContextReconstructor()` |
| Token 预算 | `from scripts import create_token_budget_manager` | `budget_manager = create_token_budget_manager(max_tokens=32000)` |
| 状态捕捉 | `from scripts import GlobalStateCapture` | `state_capture = GlobalStateCapture()` |
| 洞察模块 | `from scripts import InsightModule` | `insight = InsightModule()` |
| 链提取 | `from scripts.chains import ExtractedCausalChain, ChainType` | `chain = ExtractedCausalChain(chain_type=ChainType.CAUSAL, ...)` |
| 链缓存 | `from scripts.processors import ChainCacheManager` | `cache = ChainCacheManager(); cache.put(chain_id, chain, ChainType.CAUSAL)` |
| 监控系统 | `from scripts.processors import MonitoringSystem` | `monitor = MonitoringSystem(); monitor.record_metric("metric", 1.0)` |
| 双轨处理器 | `from scripts.processors import OptimizedDualTrackProcessor` | `processor = OptimizedDualTrackProcessor()` |
| 集成适配器 | `from scripts.processors import DualTrackIntegrationAdapter` | `adapter = DualTrackIntegrationAdapter()` |
| 链感知压缩 | `from scripts import ContextCompressor, CompressionStrategy` | `compressor = ContextCompressor(); compressor.set_chain_type_weights({...})` |

### 重要说明

1. **统一入口推荐**：使用 `create_context_orchestrator()` 创建编排器实例，这是推荐的使用方式
2. **语义桶类型**：`SemanticBucketType` 枚举用于标记记忆的类型（USER_INTENT、TOPIC、ENTITY、RELATIONSHIP、CONCEPT、EVENT、FACT）
3. **模块位置**：所有脚本位于 `scripts/` 目录，通过 `from scripts import ...` 统一导入
4. **工厂函数**：部分模块提供工厂函数（如 `create_redis_adapter`），推荐使用这些函数初始化实例
```
