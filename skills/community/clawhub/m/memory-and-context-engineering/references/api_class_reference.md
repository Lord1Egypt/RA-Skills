# API 类名速查表

本文档列出所有导出的类名及其职责，避免测试时产生误解。

## 目录

1. [核心管理器类](#一核心管理器类)
2. [洞察分析类](#二洞察分析类)
3. [状态管理类](#三状态管理类)
4. [检索相关类](#四检索相关类)
5. [记忆处理类](#五记忆处理类)
6. [异步写入类](#六异步写入类)
7. [上下文编排类](#七上下文编排类)
8. [工具类](#八工具类)
9. [加密与安全类](#九加密与安全类)
10. [数据模型类](#十数据模型类)
11. [Redis相关类](#十一redis相关类)
12. [常见误解澄清](#十二常见误解澄清)

---

## 一、核心管理器类

| 类名 | 导入路径 | 职责 | 主要方法 |
|------|----------|------|----------|
| `PerceptionMemoryStore` | `scripts.perception` | 感知记忆存储 | `create_session()`, `store_conversation()` |
| `ShortTermMemoryManager` | `scripts.short_term` | 短期记忆管理 | `store()`, `get_stats()`, `get_topic_summary()` |
| `LongTermMemoryManager` | `scripts.long_term` | 长期记忆管理 | `update_user_profile()`, `update_procedural_memory()` |
| `AsynchronousExtractor` | `scripts.short_term` | 短期→长期记忆提炼 | `extract()`, `get_stats()`, `get_last_insight()` |
| `DetachedObserver` | `scripts.insight_module` | 独立观察者 | `observe()`, `get_observations()` |

---

## 二、洞察分析类

| 类名 | 导入路径 | 职责 | 主要方法 |
|------|----------|------|----------|
| `ShortTermInsightAnalyzer` | `scripts.short_term_insight` | 短期记忆洞察分析 | `analyze()`, `get_stats()` |
| `InsightModule` | `scripts.insight_module` | 洞察生成模块 | `observe()`, `get_insights()` |
| `InsightPool` | `scripts.insight_module` | 洞察池管理 | `add()`, `get_active()`, `get_stats()` |
| `StatePatternAnalyzer` | `scripts.insight_module` | 状态模式分析 | `analyze()`, `get_patterns()` |
| `KnowledgeGapIdentifier` | `scripts.knowledge_gap_identifier` | 知识缺口识别 | `identify()`, `get_gaps()` |

---

## 三、状态管理类

| 类名 | 导入路径 | 职责 | 主要方法 |
|------|----------|------|----------|
| `GlobalStateCapture` | `scripts.state_capture` | 全局状态捕捉 | `capture()`, `create_checkpoint()`, `restore()` |
| `GlobalState` | `scripts.state_capture` | 全局状态数据模型 | - |
| `GlobalStateSnapshot` | `scripts.state_capture` | 状态快照 | - |
| `IncrementalSync` | `scripts.incremental_sync` | 增量同步 | `sync()`, `get_stats()` |
| `TaskState` | `scripts.task_progress` | 任务状态 | - |
| `TaskProgressTracker` | `scripts.task_progress` | 任务进度追踪 | `update()`, `get_progress()` |

---

## 四、检索相关类

| 类名 | 导入路径 | 职责 | 主要方法 |
|------|----------|------|----------|
| `RetrievalDecisionEngine` | `scripts.retrieval_decision_engine` | 检索决策引擎 | `decide()`, `should_retrieve()` |
| `RetrievalDecision` | `scripts.retrieval_decision_engine` | 检索决策结果 | - |
| `RetrievalNeed` | `scripts.retrieval_decision_engine` | 检索需求枚举 | - |
| `SemanticBucket` | `scripts.retrieval_decision_engine` | 语义分桶 | `add()`, `get_bucket()` |
| `SemanticBucketType` | `scripts.retrieval_decision_engine` | 分桶类型枚举 | - |
| `RetrievalOrganizer` | `scripts.retrieval_decision_engine` | 检索组织器 | `organize()`, `get_result()` |
| `OrganizedRetrieval` | `scripts.retrieval_decision_engine` | 组织化检索结果 | - |

---

## 五、记忆处理类

| 类名 | 导入路径 | 职责 | 主要方法 |
|------|----------|------|----------|
| `CausalChainExtractor` | `scripts.causal_chain_extractor` | 因果链提取 | `extract()`, `get_chains()` |
| `ExtractedCausalChain` | `scripts.causal_chain_extractor` | 提取的因果链 | - |
| `KnowledgeGapIdentifier` | `scripts.knowledge_gap_identifier` | 知识缺口识别 | `identify()`, `get_gaps()` |
| `GapAnalysisResult` | `scripts.knowledge_gap_identifier` | 缺口分析结果 | - |
| `MemoryIndexer` | `scripts.memory_index` | 记忆索引 | `index()`, `search()`, `get_stats()` |
| `ChainReasoningEnhancer` | `scripts.chain_reasoning` | 链式推理增强 | `enhance()`, `get_chain()` |
| `Insight` | `scripts.insight_module` | 洞察数据模型 | - |
| `InsightPoolData` | `scripts.insight_module` | 洞察池数据 | - |

---

## 六、异步写入类

| 类名 | 导入路径 | 职责 | 主要方法 |
|------|----------|------|----------|
| `AsyncWriter` | `scripts.async_writer` | 异步写入器 | `write()`, `get_stats()`, `flush()` |
| `BatchedWriter` | `scripts.batched_writer` | 批量写入器 | `write()`, `get_stats()`, `flush_all()` |
| `BatchedWriterConfig` | `scripts.batched_writer` | 批量写入配置 | - |
| `BatchedWriterStats` | `scripts.batched_writer` | 批量写入统计 | - |
| `WriteRequest` | `scripts.batched_writer` | 写入请求 | - |
| `WriteResult` | `scripts.batched_writer` | 写入结果 | - |
| `WriteStatus` | `scripts.batched_writer` | 写入状态枚举 | - |
| `WriterConfig` | `scripts.batched_writer` | 写入器配置 | - |
| `WriterStats` | `scripts.batched_writer` | 写入器统计 | - |

---

## 七、上下文编排类

| 类名 | 导入路径 | 职责 | 主要方法 |
|------|----------|------|----------|
| `ContextOrchestrator` | `scripts.context_orchestrator` | 上下文编排器 | `prepare()`, `get_context()` |
| `ContextReconstructor` | `scripts.context_reconstructor` | 上下文重构器 | `reconstruct()`, `get_package()` |
| `ContextBlock` | `scripts.context_orchestrator` | 上下文块 | - |
| `ContextConfig` | `scripts.context_orchestrator` | 上下文配置 | - |
| `ContextPackage` | `scripts.context_orchestrator` | 上下文包 | - |
| `ContextPriority` | `scripts.context_orchestrator` | 上下文优先级枚举 | - |
| `ContextSource` | `scripts.context_orchestrator` | 上下文来源枚举 | - |
| `PreparedContext` | `scripts.context_orchestrator` | 准备好的上下文 | - |
| `QualityEvaluator` | `scripts.context_reconstructor` | 质量评估器 | `evaluate()`, `get_scores()` |
| `WeightAdapter` | `scripts.context_reconstructor` | 权重适配器 | `adapt()`, `get_weights()` |
| `MemoryActivator` | `scripts.context_reconstructor` | 记忆激活器基类 | - |
| `TemporalActivator` | `scripts.context_reconstructor` | 时间激活器 | - |
| `SemanticActivator` | `scripts.context_reconstructor` | 语义激活器 | - |
| `ContextualActivator` | `scripts.context_reconstructor` | 上下文激活器 | - |
| `EmotionalActivator` | `scripts.context_reconstructor` | 情感激活器 | - |
| `CausalActivator` | `scripts.context_reconstructor` | 因果激活器 | - |
| `IdentityActivator` | `scripts.context_reconstructor` | 身份激活器 | - |
| `ReconstructedContext` | `scripts.context_reconstructor` | 重构的上下文 | - |

---

## 八、工具类

| 类名 | 导入路径 | 职责 | 主要方法 |
|------|----------|------|----------|
| `HeatManager` | `scripts.heat_manager` | 热度管理 | `calculate()`, `apply_policy()` |
| `HeatLevel` | `scripts.heat_manager` | 热度级别枚举 | - |
| `ConflictResolver` | `scripts.conflict_resolver` | 冲突解决 | `resolve()`, `detect_conflicts()` |
| `ConflictType` | `scripts.conflict_resolver` | 冲突类型枚举 | - |
| `ConflictSeverity` | `scripts.conflict_resolver` | 冲突严重性枚举 | - |
| `ConflictResolution` | `scripts.conflict_resolver` | 冲突解决结果 | - |
| `TokenBudgetManager` | `scripts.token_budget` | Token预算管理 | `allocate()`, `get_stats()` |
| `TokenBudgetConfig` | `scripts.token_budget` | Token预算配置 | - |
| `TokenCounter` | `scripts.token_budget` | Token计数器 | `count()`, `get_total()` |
| `TokenType` | `scripts.token_budget` | Token类型枚举 | - |
| `BudgetPolicy` | `scripts.token_budget` | 预算策略枚举 | - |

---

## 九、加密与安全类

| 类名 | 导入路径 | 职责 | 主要方法 |
|------|----------|------|----------|
| `CredentialManager` | `scripts.credential_manager` | 凭证管理器 | `store()`, `retrieve()`, `delete()` |
| `CredentialRecord` | `scripts.credential_manager` | 凭证记录 | - |
| `CredentialStorage` | `scripts.credential_manager` | 凭证存储 | - |
| `DataEncryptor` | `scripts.encryption` | 数据加密器 | `encrypt()`, `decrypt()` |
| `EncryptionConfig` | `scripts.encryption` | 加密配置 | - |
| `EncryptedData` | `scripts.encryption` | 加密数据 | - |
| `EncryptedFileStorage` | `scripts.encryption` | 加密文件存储 | `store()`, `load()`, `delete()` |
| `KeyManager` | `scripts.encryption` | 密钥管理器 | `generate()`, `rotate()`, `revoke()` |
| `KeyInfo` | `scripts.encryption` | 密钥信息 | - |
| `PrivacyManager` | `scripts.privacy` | 隐私管理器 | `check_access()`, `audit()` |
| `PrivacyConfig` | `scripts.privacy` | 隐私配置 | - |
| `PrivacyAuditLog` | `scripts.privacy` | 隐私审计日志 | - |
| `SensitiveDataDetector` | `scripts.privacy` | 敏感数据检测 | `detect()`, `get_matches()` |
| `DataClassification` | `scripts.privacy` | 数据分类 | - |
| `DataSensitivity` | `scripts.privacy` | 数据敏感度枚举 | - |
| `ConsentRecord` | `scripts.privacy` | 同意记录 | - |
| `ConsentStatus` | `scripts.privacy` | 同意状态枚举 | - |

---

## 十、Redis相关类

| 类名 | 导入路径 | 职责 | 主要方法 |
|------|----------|------|----------|
| `RedisAdapter` | `scripts.redis_adapter` | Redis适配器 | `get()`, `set()`, `delete()` |
| `RedisConfig` | `scripts.redis_adapter` | Redis配置 | - |
| `RedisKeyBuilder` | `scripts.redis_adapter` | Redis键构建器 | `build()`, `parse()` |
| `ShortTermMemoryRedis` | `scripts.short_term_redis` | 短期记忆Redis存储 | `store()`, `retrieve()`, `get_stats()` |
| `ShortTermRedisConfig` | `scripts.short_term_redis` | 短期Redis配置 | - |
| `ShortTermMemoryItemRedis` | `scripts.short_term_redis` | Redis存储项 | - |
| `ShortTermMemoryBucket` | `scripts.short_term_redis` | Redis存储桶 | - |

---

## 十一、数据模型类

### 记忆数据模型

| 类名 | 导入路径 | 说明 |
|------|----------|------|
| `PerceptionMemory` | `scripts.perception` | 感知记忆数据模型 |
| `PerceptionMemoryData` | `scripts.perception` | 感知记忆数据 |
| `ShortTermMemoryItem` | `scripts.short_term` | 短期记忆项 |
| `ShortTermMemoryItemRedis` | `scripts.short_term_redis` | Redis短期记忆项 |
| `ShortTermMemoryBucket` | `scripts.short_term_redis` | 短期记忆存储桶 |
| `LongTermMemoryContainer` | `scripts.long_term` | 长期记忆容器 |
| `MemoryDocument` | `scripts.long_term` | 记忆文档 |
| `MemoryMetadata` | `scripts.long_term` | 记忆元数据 |

### 语义记忆模型

| 类名 | 导入路径 | 说明 |
|------|----------|------|
| `SemanticMemory` | `scripts.short_term` | 语义记忆 |
| `SemanticMemoryData` | `scripts.short_term` | 语义记忆数据 |
| `NarrativeMemory` | `scripts.short_term` | 叙事记忆 |
| `NarrativeMemoryData` | `scripts.short_term` | 叙事记忆数据 |
| `EmotionalMemory` | `scripts.short_term` | 情感记忆 |
| `EmotionalMemoryData` | `scripts.short_term` | 情感记忆数据 |
| `ProceduralMemory` | `scripts.long_term` | 程序性记忆 |
| `ProceduralMemoryData` | `scripts.long_term` | 程序性记忆数据 |

### 用户相关模型

| 类名 | 导入路径 | 说明 |
|------|----------|------|
| `UserProfileMemory` | `scripts.long_term` | 用户画像记忆 |
| `UserProfileData` | `scripts.long_term` | 用户画像数据 |
| `UserCurrentState` | `scripts.state_capture` | 用户当前状态 |
| `UserStateLayer` | `scripts.state_capture` | 用户状态层 |
| `UserStateType` | `scripts.state_capture` | 用户状态类型枚举 |
| `UserDecision` | `scripts.state_capture` | 用户决策 |
| `UserPermission` | `scripts.privacy` | 用户权限 |

### 洞察相关模型

| 类名 | 导入路径 | 说明 |
|------|----------|------|
| `Insight` | `scripts.insight_module` | 洞察数据模型 |
| `InsightType` | `scripts.insight_module` | 洞察类型枚举 |
| `InsightPriority` | `scripts.insight_module` | 洞察优先级枚举 |
| `InsightSignal` | `scripts.insight_module` | 洞察信号 |
| `InsightSignalUnion` | `scripts.insight_module` | 洞察信号联合类型 |
| `ShortTermInsightResult` | `scripts.short_term_insight` | 短期洞察结果 |

### 任务相关模型

| 类名 | 导入路径 | 说明 |
|------|----------|------|
| `TaskState` | `scripts.task_progress` | 任务状态 |
| `TaskType` | `scripts.task_progress` | 任务类型枚举 |
| `TaskStep` | `scripts.task_progress` | 任务步骤 |
| `TaskContextLayer` | `scripts.task_progress` | 任务上下文层 |
| `ConversationTurn` | `scripts.context_orchestrator` | 对话轮次 |
| `CurrentTask` | `scripts.state_capture` | 当前任务 |

### 提取相关模型

| 类名 | 导入路径 | 说明 |
|------|----------|------|
| `ExtractionDecision` | `scripts.short_term` | 提取决策 |
| `ExtractionRecord` | `scripts.short_term` | 提取记录 |
| `ExtractionTrigger` | `scripts.short_term` | 提取触发器 |
| `ExtractionConfig` | `scripts.short_term` | 提取配置 |
| `ExtractionMapping` | `scripts.short_term` | 提取映射 |

### 主题相关模型

| 类名 | 导入路径 | 说明 |
|------|----------|------|
| `TopicCluster` | `scripts.short_term` | 主题簇 |
| `TopicRelation` | `scripts.short_term` | 主题关系 |

### 因果链相关模型

| 类名 | 导入路径 | 说明 |
|------|----------|------|
| `CausalChain` | `scripts.causal_chain_extractor` | 因果链 |
| `CausalNode` | `scripts.causal_chain_extractor` | 因果节点 |
| `CauseNode` | `scripts.causal_chain_extractor` | 原因节点 |
| `ProblemNode` | `scripts.causal_chain_extractor` | 问题节点 |
| `SolutionNode` | `scripts.causal_chain_extractor` | 解决方案节点 |
| `CausalRelation` | `scripts.causal_chain_extractor` | 因果关系 |
| `CausalRelationType` | `scripts.causal_chain_extractor` | 因果关系类型枚举 |

### 其他数据模型

| 类名 | 导入路径 | 说明 |
|------|----------|------|
| `MemoryType` | `scripts.type_defs` | 记忆类型枚举 |
| `MemoryCategory` | `scripts.type_defs` | 记忆类别枚举 |
| `MemoryState` | `scripts.type_defs` | 记忆状态枚举 |
| `MemoryImportance` | `scripts.type_defs` | 记忆重要性枚举 |
| `ContentType` | `scripts.type_defs` | 内容类型枚举 |
| `ActivationSource` | `scripts.type_defs` | 激活来源枚举 |
| `ActivationResult` | `scripts.type_defs` | 激活结果 |
| `ActivatedMemory` | `scripts.type_defs` | 激活的记忆 |
| `ActivatedExperiencesLayer` | `scripts.type_defs` | 激活的经验层 |

---

## 十二、常见误解澄清

### 1. 类名混淆

| ❌ 错误理解 | ✅ 正确类名 | 说明 |
|------------|------------|------|
| `ShortTermInsightExtractor` | `ShortTermInsightAnalyzer` | 不存在 Extractor 后缀的类 |
| `ShortTermManager` | `ShortTermMemoryManager` | 完整名称 |
| `LongTermManager` | `LongTermMemoryManager` | 完整名称 |
| `RetrievalQualityEvaluator` | `QualityEvaluator` | 在 `context_reconstructor` 模块中 |
| `MultiSourceCoordinator` | 不存在 | 此类未导出，使用 `ContextOrchestrator` |
| `CognitiveModelBuilder` | 不存在 | 此类未导出，使用 `ChainReasoningEnhancer` |
| `CrossSessionMemoryLinker` | 不存在 | 此类未导出 |
| `MemoryForgettingMechanism` | 不存在 | 此类未导出 |

### 2. 方法位置混淆

| 方法 | 正确所属类 | 说明 |
|------|------------|------|
| `get_stats()` | `ShortTermMemoryManager` | 支持统计方法 |
| `get_stats()` | `AsynchronousExtractor` | 支持统计方法 |
| `get_stats()` | `ShortTermInsightAnalyzer` | 支持统计方法 |
| `analyze()` | `ShortTermInsightAnalyzer` | 分析方法 |
| `extract()` | `AsynchronousExtractor` | 提取方法 |
| `observe()` | `InsightModule` / `DetachedObserver` | 观察方法 |
| `prepare()` | `ContextOrchestrator` | 准备上下文 |
| `reconstruct()` | `ContextReconstructor` | 重构上下文 |

### 3. 职责划分

```
┌─────────────────────────────────────────────────────────────┐
│                    记忆处理流程                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  对话输入                                                   │
│      │                                                      │
│      ▼                                                      │
│  ┌─────────────────────┐                                    │
│  │PerceptionMemoryStore│  → 实时对话存储                    │
│  └─────────────────────┘                                    │
│      │                                                      │
│      ▼                                                      │
│  ┌─────────────────────┐                                    │
│  │ShortTermMemoryManager│ → 语义分类存储                    │
│  └─────────────────────┘                                    │
│      │                                                      │
│      ├────────────────────────────────┐                     │
│      │                                │                     │
│      ▼                                ▼                     │
│  ┌───────────────────────┐   ┌───────────────────────┐     │
│  │ShortTermInsightAnalyzer│   │AsynchronousExtractor │     │
│  │  (分析短期记忆)        │   │  (提炼到长期记忆)    │     │
│  └───────────────────────┘   └───────────────────────┘     │
│                                      │                      │
│                                      ▼                      │
│                              ┌─────────────────────┐        │
│                              │LongTermMemoryManager│        │
│                              └─────────────────────┘        │
│                                      │                      │
│                                      ▼                      │
│                              ┌─────────────────────┐        │
│                              │   InsightModule     │        │
│                              │   (生成洞察)        │        │
│                              └─────────────────────┘        │
│                                      │                      │
│                                      ▼                      │
│                              ┌─────────────────────┐        │
│                              │    InsightPool      │        │
│                              │   (管理洞察池)      │        │
│                              └─────────────────────┘        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4. 检索决策流程

```
┌─────────────────────────────────────────────────────────────┐
│                    检索决策流程                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  查询请求                                                   │
│      │                                                      │
│      ▼                                                      │
│  ┌─────────────────────────┐                                │
│  │RetrievalDecisionEngine  │  → 决策是否需要检索            │
│  └─────────────────────────┘                                │
│      │                                                      │
│      ▼ (需要检索)                                           │
│  ┌─────────────────────────┐                                │
│  │   MemoryIndexer        │  → 索引搜索                    │
│  └─────────────────────────┘                                │
│      │                                                      │
│      ▼                                                      │
│  ┌─────────────────────────┐                                │
│  │ RetrievalOrganizer     │  → 组织检索结果                │
│  └─────────────────────────┘                                │
│      │                                                      │
│      ▼                                                      │
│  ┌─────────────────────────┐                                │
│  │ ContextReconstructor   │  → 重构上下文                  │
│  └─────────────────────────┘                                │
│      │                                                      │
│      ▼                                                      │
│  ┌─────────────────────────┐                                │
│  │ QualityEvaluator       │  → 质量评估                    │
│  └─────────────────────────┘                                │
│      │                                                      │
│      ▼                                                      │
│  ┌─────────────────────────┐                                │
│  │ ContextOrchestrator     │  → 编排最终上下文              │
│  └─────────────────────────┘                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 5. 导入路径说明

所有类都通过 `scripts` 模块的 `__init__.py` 导出，可以直接从 `scripts` 导入：

```python
# ✅ 正确导入方式
from scripts import (
    PerceptionMemoryStore,
    ShortTermMemoryManager,
    LongTermMemoryManager,
    InsightModule,
    # ...
)

# ❌ 错误导入方式（虽然代码中存在这些模块，但应从 scripts 导入）
from scripts.perception import PerceptionMemoryStore  # 不推荐
from scripts.short_term import ShortTermMemoryManager  # 不推荐
```

### 6. 工厂函数

除了类之外，以下工厂函数也直接从 `scripts` 导出：

| 函数名 | 职责 | 返回类型 |
|--------|------|----------|
| `create_context_orchestrator()` | 创建上下文编排器 | `ContextOrchestrator` |
| `create_chain_reasoning_enhancer()` | 创建链式推理增强器 | `ChainReasoningEnhancer` |
| `create_credential_manager()` | 创建凭证管理器 | `CredentialManager` |
| `create_redis_adapter()` | 创建Redis适配器 | `RedisAdapter` |
| `create_short_term_redis()` | 创建短期Redis存储 | `ShortTermMemoryRedis` |
| `create_token_budget_manager()` | 创建Token预算管理器 | `TokenBudgetManager` |
| `get_async_writer()` | 获取异步写入器 | `AsyncWriter` |
| `get_long_term_writer()` | 获取长期写入器 | `BatchedWriter` |
| `get_state_sync_writer()` | 获取状态同步写入器 | `BatchedWriter` |
| `shutdown_async_writer()` | 关闭异步写入器 | `None` |

### 7. 工具函数

以下工具函数可直接用于数据加密：

| 函数名 | 职责 |
|--------|------|
| `encrypt_data_with_password()` | 使用密码加密数据 |
| `decrypt_data_with_password()` | 使用密码解密数据 |
| `generate_encryption_key()` | 生成加密密钥 |

### 8. 未导出的类

以下类在代码中存在但未从 `scripts` 导出，不应在API中使用：

- `StateConsistencyValidator`
- `StateInferenceEngine`
- `CognitiveModelBuilder`
- `CrossSessionMemoryLinker`
- `MemoryForgettingMechanism`
- `MultiSourceCoordinator`

如果需要这些功能，请使用已导出的替代类或组合使用现有API。

---

## 附录：快速查询

### 按字母顺序排列的导出类列表

`ActivatedExperiencesLayer`, `ActivatedMemory`, `ActivationResult`, `ActivationSource`, `AsyncTask`, `AsyncWriter`, `AsynchronousExtractor`, `AttitudeTendency`, `BatchedWriter`, `BatchedWriterConfig`, `BatchedWriterStats`, `BudgetPolicy`, `CausalChainExtractor`, `ChainReasoningEnhancer`, `CheckpointRecord`, `CommunicationStyle`, `ConceptDefinition`, `ConfidenceMixin`, `ConflictResolution`, `ConflictResolver`, `ConflictSeverity`, `ConflictType`, `ConsentRecord`, `ConsentStatus`, `ContextAnchors`, `ContextBlock`, `ContextConfig`, `ContextEnhancement`, `ContextOrchestrator`, `ContextPackage`, `ContextPriority`, `ContextReconstructor`, `ContextSource`, `ConversationTurn`, `CredentialManager`, `CredentialRecord`, `CredentialStorage`, `CurrentTask`, `DataClassification`, `DataEncryptor`, `DataSensitivity`, `DecisionPattern`, `DecisionPatternRecord`, `DecisionSupportSignal`, `DecisionType`, `DetachedObserver`, `EmotionState`, `EmotionalContextLayer`, `EmotionalMemory`, `EmotionalMemoryData`, `EncryptedData`, `EncryptedFileStorage`, `EncryptionConfig`, `ExtractedCausalChain`, `ExtractionDecision`, `ExtractionMapping`, `ExtractionRecord`, `ExtractionTrigger`, `FitScores`, `GapAnalysisResult`, `GlobalState`, `GlobalStateCapture`, `GlobalStateSnapshot`, `GrowthMilestone`, `HeatLevel`, `HeatManager`, `HeatMixin`, `IdentityEvolution`, `IncrementalSync`, `IndexStats`, `Insight`, `InsightModule`, `InsightPool`, `InsightPoolData`, `InsightPriority`, `InsightSignal`, `InsightSignalUnion`, `InsightType`, `KeyInfo`, `KeyManager`, `KnowledgeContextLayer`, `KnowledgeEntity`, `KnowledgeGapIdentifier`, `KnowledgeType`, `LearningValue`, `LongTermMemoryContainer`, `LongTermMemoryManager`, `MemoryCategory`, `MemoryConflict`, `MemoryConflictExtended`, `MemoryDocument`, `MemoryIndexer`, `MemoryType`, `MetaLearningSample`, `ModuleState`, `NarrativeAnchorLayer`, `NarrativeMemory`, `NarrativeMemoryData`, `NeuroticismTendency`, `PerceptionMemory`, `PerceptionMemoryData`, `PerceptionMemoryStore`, `PhaseType`, `PreparedContext`, `Principle`, `PrivacyAuditLog`, `PrivacyConfig`, `PrivacyManager`, `ProblemSolvingStrategy`, `ProceduralMemory`, `ProceduralMemoryData`, `QualityDimension`, `QualityEvaluator`, `QualityScores`, `ReasoningStepWithReflection`, `ReconstructedContext`, `RedisAdapter`, `RedisConfig`, `RedisKeyBuilder`, `ReflectionMemoryItem`, `ReflectionOutcome`, `ReflectionProcessResult`, `ReflectionSeverity`, `ReflectionSignal`, `ReflectionTriggerRecord`, `ReflectionTriggerType`, `ResolutionMode`, `ResolutionResult`, `RetentionPeriod`, `RetrievalDecision`, `RetrievalDecisionEngine`, `RetrievalNeed`, `RiskAlertSignal`, `SatisfactionRecord`, `ScenarioType`, `SceneContext`, `SearchResult`, `SemanticBucket`, `SemanticBucketType`, `SemanticMemory`, `SemanticMemoryData`, `SensitiveDataDetector`, `ShortTermInsightAnalyzer`, `ShortTermInsightResult`, `ShortTermMemoryBucket`, `ShortTermMemoryItem`, `ShortTermMemoryItemRedis`, `ShortTermMemoryManager`, `ShortTermMemoryRedis`, `ShortTermRedisConfig`, `SignalStrength`, `SignalType`, `SituationAwareness`, `StateChangeEvent`, `StateEventType`, `StateSubscription`, `StoragePolicy`, `SyncState`, `SyncStats`, `SyncStatus`, `TaskContextLayer`, `TaskState`, `TaskType`, `TechnicalBackground`, `TemporaryContext`, `TextProcessor`, `TimestampMixin`, `TimingHintSignal`, `TokenBudgetConfig`, `TokenBudgetManager`, `TokenCounter`, `TokenType`, `ToolCombinationPattern`, `ToolOptimalContext`, `ToolRecommendationSignal`, `ToolUsageRecord`, `TopicCluster`, `TopicRelation`, `TriggerDimension`, `UserCurrentState`, `UserDecision`, `UserProfileData`, `UserProfileMemory`, `UserStateLayer`, `UserStateType`, `VerificationResult`, `WeightAdapter`, `WeightConfig`, `WriterConfig`, `WriterStats`

### 按字母顺序排列的导出函数列表

`create_chain_reasoning_enhancer()`, `create_context_orchestrator()`, `create_credential_manager()`, `create_redis_adapter()`, `create_short_term_redis()`, `create_token_budget_manager()`, `decrypt_data_with_password()`, `encrypt_data_with_password()`, `generate_encryption_key()`, `get_async_writer()`, `get_long_term_writer()`, `get_state_sync_writer()`, `shutdown_async_writer()`
