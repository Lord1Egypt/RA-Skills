# scripts 类名速查表（自动生成）

> **本文档由 `generate-api-docs.py` 自动生成**，以代码为唯一真相源。
> 列出全部可导入类、枚举与函数及其真实所在模块。

## 导出符号总表

| 符号 | 类型 | 真实模块 | 职责/说明 |
|------|------|----------|-----------|
| `__version__` | 常量 | `unknown` | str(object='') -> str |
| `SemanticBucketType` | 枚举 | `scripts.type_defs` | 语义分类桶类型 |
| `PerceptionMemoryStore` | 类 | `scripts.perception` | 感知记忆存储 |
| `SemanticBucket` | 类 | `scripts.short_term` | 语义分类桶 |
| `ShortTermMemoryManager` | 类 | `scripts.short_term` | 短期记忆管理器 |
| `AsynchronousExtractor` | 类 | `scripts.short_term` | 异步提炼器（洞察驱动版） |
| `TopicCluster` | 类 | `scripts.short_term_insight` | 话题簇 |
| `TopicRelation` | 类 | `scripts.short_term_insight` | 话题关联 |
| `ExtractionDecision` | 类 | `scripts.short_term_insight` | 提炼决策 |
| `ShortTermInsightResult` | 类 | `scripts.short_term_insight` | 短期洞察结果 |
| `ShortTermInsightAnalyzer` | 类 | `scripts.short_term_insight` | 短期记忆洞察分析器 |
| `LongTermMemoryManager` | 类 | `scripts.long_term` | 长期记忆管理器 |
| `QualityEvaluator` | 类 | `scripts.context_reconstructor` | 六维质量评估器 |
| `WeightAdapter` | 类 | `scripts.context_reconstructor` | 比重适配器 |
| `ContextReconstructor` | 类 | `scripts.context_reconstructor` | 上下文重构器 |
| `InsightPool` | 类 | `scripts.insight_module` | 洞察池 |
| `DetachedObserver` | 类 | `scripts.insight_module` | 超然观察者 |
| `InsightModule` | 类 | `scripts.insight_module` | 独立洞察模块 |
| `GlobalStateCapture` | 类 | `scripts.state_capture` | 全局状态捕捉器 |
| `GlobalState` | 类 | `scripts.type_defs` | 全局状态 |
| `GlobalStateSnapshot` | 类 | `scripts.type_defs` | 全局状态快照 |
| `HeatManager` | 类 | `scripts.heat_manager` | 记忆冷热度管理器 |
| `ConflictResolver` | 类 | `scripts.conflict_resolver` | 冲突解决器 |
| `ConsentStatus` | 枚举 | `scripts.privacy_consent` | 同意状态 |
| `DataSensitivity` | 枚举 | `scripts.privacy` | 数据敏感度级别 |
| `StoragePolicy` | 枚举 | `scripts.privacy` | 存储策略 |
| `RetentionPeriod` | 枚举 | `scripts.privacy` | 保留期限 |
| `ConsentRecord` | 类 | `scripts.privacy_consent` | 同意记录 |
| `PrivacyConfig` | 类 | `scripts.privacy` | 隐私配置 |
| `DataClassification` | 类 | `scripts.privacy` | 数据分类结果 |
| `PrivacyAuditLog` | 类 | `scripts.privacy` | 隐私审计日志 |
| `SensitiveDataDetector` | 类 | `scripts.privacy` | 敏感数据检测器 |
| `PrivacyManager` | 类 | `scripts.privacy` | 隐私管理器 |
| `PRIVACY_NOTICE_TEMPLATE` | 常量 | `unknown` | str(object='') -> str |
| `EncryptedData` | 类 | `scripts.encryption` | 加密数据容器 |
| `KeyInfo` | 类 | `scripts.encryption` | 密钥信息（不包含实际密钥） |
| `EncryptionConfig` | 类 | `scripts.encryption` | 加密配置 |
| `KeyManager` | 类 | `scripts.encryption` | 密钥管理器 |
| `DataEncryptor` | 类 | `scripts.encryption` | 数据加密器 |
| `EncryptedFileStorage` | 类 | `scripts.encryption` | 加密文件存储 |
| `encrypt_data_with_password` | 函数 | `scripts.encryption` | 使用密码加密数据 |
| `decrypt_data_with_password` | 函数 | `scripts.encryption` | 使用密码解密数据 |
| `generate_encryption_key` | 函数 | `scripts.encryption` | 生成加密密钥（Base64 编码） |
| `CRYPTO_AVAILABLE` | 常量 | `unknown` | Returns True when the argument is true, False otherwise. |
| `TextProcessor` | 类 | `scripts.memory_index` | 文本处理器 |
| `MemoryIndexer` | 类 | `scripts.memory_index` | 记忆索引器 |
| `MemoryDocument` | 类 | `scripts.memory_index` | 记忆文档（用于索引） |
| `SearchResult` | 类 | `scripts.memory_index` | 检索结果 |
| `IndexStats` | 类 | `scripts.memory_index` | 索引统计 |
| `SyncStatus` | 枚举 | `scripts.incremental_sync` | 同步状态 |
| `SyncState` | 类 | `scripts.incremental_sync` | 同步状态 |
| `ExtractionRecord` | 类 | `scripts.incremental_sync` | 提炼记录 |
| `SyncStats` | 类 | `scripts.incremental_sync` | 同步统计 |
| `IncrementalSync` | 类 | `scripts.incremental_sync` | 增量同步器 |
| `CredentialRecord` | 类 | `scripts.credential_manager` | 凭证记录（元数据，不含明文） |
| `CredentialStorage` | 类 | `scripts.credential_manager` | 凭证存储结构 |
| `CredentialManager` | 类 | `scripts.credential_manager` | 凭证管理器 |
| `create_credential_manager` | 函数 | `scripts.credential_manager` | 创建凭证管理器的便捷函数 |
| `ChainReasoningEnhancer` | 类 | `scripts.chain_reasoning` | 链式推理增强模块 |
| `create_chain_reasoning_enhancer` | 函数 | `scripts.chain_reasoning` | 创建链式推理增强器实例 |
| `extract_causal_chains` | 函数 | `scripts.chain_reasoning` | 从上下文中提取因果链 |
| `ExtractedCausalChain` | 类 | `scripts.chains.causal_chain` | 因果链：问题→原因→解决方案 |
| `ExtractedLogicChain` | 类 | `scripts.chains.logic_chain` | 逻辑链：前提→推理→结论 |
| `ExtractedOperationChain` | 类 | `scripts.chains.operation_chain` | 操作链：动作1→动作2→结果 |
| `ExtractedNarrativeChain` | 类 | `scripts.chains.narrative_chain` | 叙事链：事件1→事件2→事件3 |
| `ExtractedTimeChain` | 类 | `scripts.chains.time_chain` | 时间链：时间点A→时间点B→时间点C |
| `ChainBuffer` | 类 | `scripts.chains.chain_buffer` | 链缓冲区（独立的链存储空间） |
| `ChainType` | 枚举 | `scripts.chains.base_chain` | 链类型枚举 |
| `BaseExtractedChain` | 类 | `scripts.chains.base_chain` | 提取链的基类 |
| `REDIS_AVAILABLE` | 常量 | `unknown` | Returns True when the argument is true, False otherwise. |
| `RedisConfig` | 类 | `scripts.redis_adapter` | Redis 连接配置（安全增强版） |
| `RedisKeyBuilder` | 类 | `scripts.redis_adapter` | Redis Key 命名工具 |
| `RedisAdapter` | 类 | `scripts.redis_adapter` | Redis 适配器 |
| `create_redis_adapter` | 函数 | `scripts.redis_adapter` | 创建 Redis 适配器 |
| `ShortTermMemoryItemRedis` | 类 | `scripts.short_term_redis` | 短期记忆项（Redis 存储格式） |
| `ShortTermRedisConfig` | 类 | `scripts.short_term_redis` | 短期记忆 Redis 配置 |
| `ShortTermMemoryRedis` | 类 | `scripts.short_term_redis` | 短期记忆 Redis 存储 |
| `create_short_term_redis` | 函数 | `scripts.short_term_redis` | 创建短期记忆 Redis 存储 |
| `TokenType` | 枚举 | `scripts.token_budget` | Token 类型 |
| `BudgetPolicy` | 枚举 | `scripts.token_budget` | 预算策略 |
| `TokenBudgetConfig` | 类 | `scripts.token_budget` | Token 预算配置 |
| `TokenCounter` | 类 | `scripts.token_budget` | Token 计数器 |
| `TokenBudgetManager` | 类 | `scripts.token_budget` | Token 预算管理器 |
| `create_token_budget_manager` | 函数 | `scripts.token_budget` | 创建 Token 预算管理器 |
| `ContextPriority` | 枚举 | `scripts.context_orchestrator` | 上下文优先级 |
| `ContextSource` | 枚举 | `scripts.context_orchestrator` | 上下文来源 |
| `ContextBlock` | 类 | `scripts.context_orchestrator` | 上下文块 |
| `ContextConfig` | 类 | `scripts.context_orchestrator` | Context Orchestrator 配置 |
| `PreparedContext` | 类 | `scripts.context_orchestrator` | 准备好的上下文 |
| `ContextOrchestrator` | 类 | `scripts.context_orchestrator` | 上下文编排器（总控层） |
| `create_context_orchestrator` | 函数 | `scripts.context_orchestrator` | 创建上下文编排器 |
| `ContextCompressor` | 类 | `scripts.context_orchestrator` | 上下文压缩器 |
| `CompressionStrategy` | 枚举 | `scripts.context_orchestrator` | 压缩策略 |
| `PriorityResolver` | 类 | `scripts.context_orchestrator` | 优先级解析器（优化版） |
| `MetadataQualityAssessor` | 类 | `scripts.context_orchestrator` | Metadata 质量评估器 |
| `CustomTypeLifecycleManager` | 类 | `scripts.context_orchestrator` | 自定义类型生命周期管理器 |
| `UsageMonitor` | 类 | `scripts.context_orchestrator` | 使用情况监控器 |
| `LRUCache` | 类 | `scripts.context_orchestrator` | LRU（最近最少使用）缓存实现 |
| `PerformanceMonitor` | 类 | `scripts.context_orchestrator` | 性能监控器 |
| `BatchProcessor` | 类 | `scripts.context_orchestrator` | 批量处理器 |
| `ContextPackage` | 类 | `scripts.type_defs` | 上下文包 |
| `AsyncWriter` | 类 | `scripts.async_writer` | 异步写入器 |
| `WriterConfig` | 类 | `scripts.async_writer` | 写入器配置 |
| `WriterStats` | 类 | `scripts.async_writer` | 写入器统计 |
| `get_async_writer` | 函数 | `scripts.async_writer` | 获取全局异步写入器 |
| `shutdown_async_writer` | 函数 | `scripts.async_writer` | 关闭全局异步写入器 |
| `BatchedWriter` | 类 | `scripts.batched_writer` | 批量写入器 |
| `BatchedWriterConfig` | 类 | `scripts.batched_writer` | 批量写入器配置 |
| `BatchedWriterStats` | 类 | `scripts.batched_writer` | 批量写入器统计 |
| `get_long_term_writer` | 函数 | `scripts.batched_writer` | 获取长期记忆批量写入器 |
| `get_state_sync_writer` | 函数 | `scripts.batched_writer` | 获取状态同步批量写入器 |
| `PathSecurity` | 类 | `scripts.path_security` | 路径安全验证器 |
| `PathSecurityError` | 类 | `scripts.path_security` | 路径安全错误 |
| `IntentSafetyManager` | 类 | `scripts.intent_safety_manager` | 意图安全与审计管理器 |
| `OperationType` | 枚举 | `scripts.intent_safety_manager` | 操作类型枚举 |
| `PermissionLevel` | 枚举 | `scripts.intent_safety_manager` | 用户权限级别 |
| `ToolOutputSanitizer` | 类 | `scripts.tool_output_sanitizer` | 工具输出清洗器 |
| `PrivacyConsent` | 类 | `scripts.privacy_consent` | 增强的隐私同意管理器 |
| `ConsentStatus` | 枚举 | `scripts.privacy_consent` | 同意状态 |
| `get_logger` | 函数 | `scripts.logging_config` | 获取模块日志器 |
| `set_log_level` | 函数 | `scripts.logging_config` | 动态设置日志级别 |
| `set_log_format` | 函数 | `scripts.logging_config` | 动态设置日志格式 |
| `AgentMemoryConfig` | 类 | `scripts.config` | Agent Memory System 统一配置 |
| `get_config` | 函数 | `scripts.config` | 获取全局配置实例 |
| `reload_config` | 函数 | `scripts.config` | 重新加载配置 |
| `BenchmarkRunner` | 类 | `scripts.benchmark` | 基准测试运行器 |
| `BenchmarkResult` | 类 | `scripts.benchmark` | 基准测试结果 |
| `CausalRelationType` | 枚举 | `scripts.causal_chain_extractor` | 因果关系类型 |
| `ProblemType` | 枚举 | `scripts.causal_chain_extractor` | 问题类型 |
| `SolutionStatus` | 枚举 | `scripts.causal_chain_extractor` | 解决方案状态 |
| `CausalNode` | 类 | `scripts.causal_chain_extractor` | 因果节点 |
| `CausalRelation` | 类 | `scripts.causal_chain_extractor` | 因果关系 |
| `ProblemNode` | 类 | `scripts.causal_chain_extractor` | 问题节点 |
| `CauseNode` | 类 | `scripts.causal_chain_extractor` | 原因节点 |
| `SolutionNode` | 类 | `scripts.causal_chain_extractor` | 解决方案节点 |
| `ExtractedCausalChain` | 类 | `scripts.causal_chain_extractor` | 提取的因果链 |
| `ExtractionConfig` | 类 | `scripts.causal_chain_extractor` | 提取配置 |
| `CausalChainExtractor` | 类 | `scripts.causal_chain_extractor` | 因果链提取器 |
| `create_causal_extractor` | 函数 | `scripts.causal_chain_extractor` | 创建因果链提取器 |
| `BaseExtractedChain` | 类 | `scripts.chains.base_chain` | 提取链的基类 |
| `ChainType` | 枚举 | `scripts.chains.base_chain` | 链类型枚举 |
| `ExtractedCausalChain` | 类 | `scripts.chains.causal_chain` | 因果链：问题→原因→解决方案 |
| `ProblemNode` | 类 | `scripts.chains.causal_chain` | 问题节点 |
| `CauseNode` | 类 | `scripts.chains.causal_chain` | 原因节点 |
| `CausalRelation` | 类 | `scripts.chains.causal_chain` | 因果关系 |
| `SolutionNode` | 类 | `scripts.chains.causal_chain` | 解决方案节点 |
| `ExtractedLogicChain` | 类 | `scripts.chains.logic_chain` | 逻辑链：前提→推理→结论 |
| `ExtractedOperationChain` | 类 | `scripts.chains.operation_chain` | 操作链：动作1→动作2→结果 |
| `ExtractedNarrativeChain` | 类 | `scripts.chains.narrative_chain` | 叙事链：事件1→事件2→事件3 |
| `ExtractedTimeChain` | 类 | `scripts.chains.time_chain` | 时间链：时间点A→时间点B→时间点C |
| `ChainBuffer` | 类 | `scripts.chains.chain_buffer` | 链缓冲区（独立的链存储空间） |
| `ChainExtractor` | 类 | `scripts.chains.chain_extractor` | 链提取器（统一入口） |
| `BaseExtractor` | 类 | `scripts.chains.extractors.base_extractor` | 链提取器基类 |
| `CausalExtractor` | 类 | `scripts.chains.extractors.causal_extractor` | 因果链提取器 |
| `LogicExtractor` | 类 | `scripts.chains.extractors.logic_extractor` | 逻辑链提取器 |
| `OperationExtractor` | 类 | `scripts.chains.extractors.operation_extractor` | 操作链提取器 |
| `NarrativeExtractor` | 类 | `scripts.chains.extractors.narrative_extractor` | 叙事链提取器 |
| `TimeExtractor` | 类 | `scripts.chains.extractors.time_extractor` | 时间链提取器 |
| `ExtractionResult` | 类 | `scripts.chains.extractors.base_extractor` | 提取结果 |
| `BaseExtractor` | 类 | `scripts.chains.extractors.base_extractor` | 链提取器基类 |
| `ExtractionResult` | 类 | `scripts.chains.extractors.base_extractor` | 提取结果 |
| `CausalExtractor` | 类 | `scripts.chains.extractors.causal_extractor` | 因果链提取器 |
| `LogicExtractor` | 类 | `scripts.chains.extractors.logic_extractor` | 逻辑链提取器 |
| `OperationExtractor` | 类 | `scripts.chains.extractors.operation_extractor` | 操作链提取器 |
| `NarrativeExtractor` | 类 | `scripts.chains.extractors.narrative_extractor` | 叙事链提取器 |
| `TimeExtractor` | 类 | `scripts.chains.extractors.time_extractor` | 时间链提取器 |
| `StepResult` | 枚举 | `scripts.cognitive_model_builder` | 步骤结果 |
| `FactSource` | 枚举 | `scripts.cognitive_model_builder` | 事实来源 |
| `ConstraintType` | 枚举 | `scripts.cognitive_model_builder` | 约束类型 |
| `GapImportance` | 枚举 | `scripts.cognitive_model_builder` | 知识缺口重要程度 |
| `DecisionStatus` | 枚举 | `scripts.cognitive_model_builder` | 决策状态 |
| `TaskContext` | 类 | `scripts.cognitive_model_builder` | 任务上下文 - 模型需要知道的"我在哪里、我要去哪里" |
| `PathStep` | 类 | `scripts.cognitive_model_builder` | 路径步骤 - 模型需要知道的"我怎么走到这里" |
| `Constraint` | 类 | `scripts.cognitive_model_builder` | 约束条件 - 模型需要知道的"边界" |
| `ConstraintSet` | 类 | `scripts.cognitive_model_builder` | 约束集 |
| `Fact` | 类 | `scripts.cognitive_model_builder` | 事实 - 模型需要知道的"我知道什么" |
| `Hypothesis` | 类 | `scripts.cognitive_model_builder` | 假设 - 模型需要知道的"我假设什么" |
| `KnowledgeGap` | 类 | `scripts.cognitive_model_builder` | 知识缺口 - 模型需要知道的"我不知道什么" |
| `DecisionOption` | 类 | `scripts.cognitive_model_builder` | 决策选项 |
| `DecisionPoint` | 类 | `scripts.cognitive_model_builder` | 决策点 - 模型需要知道的"我需要决定什么" |
| `CausalChain` | 类 | `scripts.cognitive_model_builder` | 因果链 - 模型需要知道的"因果关系" |
| `CognitiveModel` | 类 | `scripts.cognitive_model_builder` | 认知模型 - 模型可高效理解和推理的结构 |
| `CognitiveModelBuilder` | 类 | `scripts.cognitive_model_builder` | 认知模型构建器 |
| `create_cognitive_model` | 函数 | `scripts.cognitive_model_builder` | 创建空白认知模型 |
| `create_cognitive_builder` | 函数 | `scripts.cognitive_model_builder` | 创建认知模型构建器 |
| `ConflictResolver` | 类 | `scripts.conflict_resolver` | 冲突解决器 |
| `LoadPriority` | 枚举 | `scripts.context_lazy_loader` | 加载优先级 |
| `LoadStatus` | 枚举 | `scripts.context_lazy_loader` | 加载状态 |
| `PredictStrategy` | 枚举 | `scripts.context_lazy_loader` | 预加载策略 |
| `LoadRequest` | 类 | `scripts.context_lazy_loader` | 加载请求 |
| `LoadResult` | 类 | `scripts.context_lazy_loader` | 加载结果 |
| `CacheEntry` | 类 | `scripts.context_lazy_loader` | 缓存条目 |
| `LoaderConfig` | 类 | `scripts.context_lazy_loader` | 懒加载器配置 |
| `LoaderStats` | 类 | `scripts.context_lazy_loader` | 加载器统计 |
| `LRUCache` | 类 | `scripts.context_lazy_loader` | LRU 缓存实现 |
| `PriorityQueue` | 类 | `scripts.context_lazy_loader` | 优先级队列 |
| `ContextLazyLoader` | 类 | `scripts.context_lazy_loader` | 上下文懒加载器 |
| `create_lazy_loader` | 函数 | `scripts.context_lazy_loader` | 创建懒加载器 |
| `ContextPriority` | 枚举 | `scripts.context_orchestrator` | 上下文优先级 |
| `ContextSource` | 枚举 | `scripts.context_orchestrator` | 上下文来源 |
| `ContextBlock` | 类 | `scripts.context_orchestrator` | 上下文块 |
| `ContextConfig` | 类 | `scripts.context_orchestrator` | Context Orchestrator 配置 |
| `PreparedContext` | 类 | `scripts.context_orchestrator` | 准备好的上下文 |
| `ContextOrchestrator` | 类 | `scripts.context_orchestrator` | 上下文编排器（总控层） |
| `create_context_orchestrator` | 函数 | `scripts.context_orchestrator` | 创建上下文编排器 |
| `CompressionStrategy` | 枚举 | `scripts.context_orchestrator` | 压缩策略 |
| `CompressionResult` | 类 | `scripts.context_orchestrator` | 压缩结果 |
| `ContextCompressor` | 类 | `scripts.context_orchestrator` | 上下文压缩器 |
| `MetadataValidator` | 类 | `scripts.context_orchestrator` | Metadata 验证器 |
| `ValidationResult` | 类 | `scripts.context_orchestrator` | 验证结果 |
| `PriorityResolver` | 类 | `scripts.context_orchestrator` | 优先级解析器（优化版） |
| `QualityAssessment` | 类 | `scripts.context_orchestrator` | 质量评估结果 |
| `MetadataQualityAssessor` | 类 | `scripts.context_orchestrator` | Metadata 质量评估器 |
| `CustomTypeLifecycleManager` | 类 | `scripts.context_orchestrator` | 自定义类型生命周期管理器 |
| `UsageMonitor` | 类 | `scripts.context_orchestrator` | 使用情况监控器 |
| `QualityReportGenerator` | 类 | `scripts.context_orchestrator` | 质量报告生成器 |
| `LRUCache` | 类 | `scripts.context_orchestrator` | LRU（最近最少使用）缓存实现 |
| `PerformanceMonitor` | 类 | `scripts.context_orchestrator` | 性能监控器 |
| `BatchProcessor` | 类 | `scripts.context_orchestrator` | 批量处理器 |
| `QualityEvaluator` | 类 | `scripts.context_reconstructor` | 六维质量评估器 |
| `WeightAdapter` | 类 | `scripts.context_reconstructor` | 比重适配器 |
| `MemoryActivator` | 类 | `scripts.context_reconstructor` | 记忆激活器基类 |
| `TemporalActivator` | 类 | `scripts.context_reconstructor` | 时间激活器 |
| `SemanticActivator` | 类 | `scripts.context_reconstructor` | 语义激活器 |
| `ContextualActivator` | 类 | `scripts.context_reconstructor` | 情境激活器 |
| `EmotionalActivator` | 类 | `scripts.context_reconstructor` | 情感激活器 |
| `CausalActivator` | 类 | `scripts.context_reconstructor` | 因果激活器 |
| `IdentityActivator` | 类 | `scripts.context_reconstructor` | 身份激活器 |
| `ContextReconstructor` | 类 | `scripts.context_reconstructor` | 上下文重构器 |
| `LinkStrength` | 枚举 | `scripts.cross_session_memory_linker` | 关联强度 |
| `LinkType` | 枚举 | `scripts.cross_session_memory_linker` | 关联类型 |
| `SessionStatus` | 枚举 | `scripts.cross_session_memory_linker` | 会话状态 |
| `SessionNode` | 类 | `scripts.cross_session_memory_linker` | 会话节点 |
| `MemoryLink` | 类 | `scripts.cross_session_memory_linker` | 记忆关联 |
| `KnowledgeTransfer` | 类 | `scripts.cross_session_memory_linker` | 知识迁移 |
| `SessionGraph` | 类 | `scripts.cross_session_memory_linker` | 会话图谱 |
| `LinkerConfig` | 类 | `scripts.cross_session_memory_linker` | 关联器配置 |
| `CrossSessionMemoryLinker` | 类 | `scripts.cross_session_memory_linker` | 跨会话记忆关联器 |
| `create_session_linker` | 函数 | `scripts.cross_session_memory_linker` | 创建跨会话记忆关联器 |
| `KEY_LENGTH` | 常量 | `unknown` | int([x]) -> integer |
| `NONCE_LENGTH` | 常量 | `unknown` | int([x]) -> integer |
| `TAG_LENGTH` | 常量 | `unknown` | int([x]) -> integer |
| `KDF_ITERATIONS` | 常量 | `unknown` | int([x]) -> integer |
| `SALT_LENGTH` | 常量 | `unknown` | int([x]) -> integer |
| `EncryptedData` | 类 | `scripts.encryption` | 加密数据容器 |
| `KeyInfo` | 类 | `scripts.encryption` | 密钥信息（不包含实际密钥） |
| `EncryptionConfig` | 类 | `scripts.encryption` | 加密配置 |
| `KeyManager` | 类 | `scripts.encryption` | 密钥管理器 |
| `DataEncryptor` | 类 | `scripts.encryption` | 数据加密器 |
| `EncryptedFileStorage` | 类 | `scripts.encryption` | 加密文件存储 |
| `encrypt_data_with_password` | 函数 | `scripts.encryption` | 使用密码加密数据 |
| `decrypt_data_with_password` | 函数 | `scripts.encryption` | 使用密码解密数据 |
| `generate_encryption_key` | 函数 | `scripts.encryption` | 生成加密密钥（Base64 编码） |
| `CRYPTO_AVAILABLE` | 常量 | `unknown` | Returns True when the argument is true, False otherwise. |
| `BucketChainLinker` | 类 | `scripts.fusion.bucket_chain_linker` | 桶-链关联器 |
| `BucketChainLink` | 类 | `scripts.fusion.bucket_chain_linker` | 桶-链关联 |
| `CrossValidator` | 类 | `scripts.fusion.cross_validator` | 交叉验证器 |
| `ValidationResult` | 类 | `scripts.fusion.cross_validator` | 验证结果 |
| `MultiDimensionSummaryGenerator` | 类 | `scripts.fusion.multi_dimension_summary` | 多维摘要生成器 |
| `MultiDimensionSummary` | 类 | `scripts.fusion.multi_dimension_summary` | 多维摘要 |
| `BucketChainFusion` | 类 | `scripts.fusion.bucket_chain_fusion` | 桶-链融合层 |
| `HeatManager` | 类 | `scripts.heat_manager` | 记忆冷热度管理器 |
| `SyncStatus` | 枚举 | `scripts.incremental_sync` | 同步状态 |
| `SyncState` | 类 | `scripts.incremental_sync` | 同步状态 |
| `ExtractionRecord` | 类 | `scripts.incremental_sync` | 提炼记录 |
| `SyncStats` | 类 | `scripts.incremental_sync` | 同步统计 |
| `IncrementalSync` | 类 | `scripts.incremental_sync` | 增量同步器 |
| `InsightPool` | 类 | `scripts.insight_module` | 洞察池 |
| `DetachedObserver` | 类 | `scripts.insight_module` | 超然观察者 |
| `InsightModule` | 类 | `scripts.insight_module` | 独立洞察模块 |
| `StatePatternAnalyzer` | 类 | `scripts.insight_module` | 状态模式分析器 |
| `KnowledgeType` | 枚举 | `scripts.knowledge_gap_identifier` | 知识类型 |
| `GapCategory` | 枚举 | `scripts.knowledge_gap_identifier` | 缺口类别 |
| `FillStrategy` | 枚举 | `scripts.knowledge_gap_identifier` | 填充策略 |
| `BlockingLevel` | 枚举 | `scripts.knowledge_gap_identifier` | 阻塞级别 |
| `KnowledgeItem` | 类 | `scripts.knowledge_gap_identifier` | 知识项 |
| `RequiredKnowledge` | 类 | `scripts.knowledge_gap_identifier` | 所需知识 |
| `IdentifiedGap` | 类 | `scripts.knowledge_gap_identifier` | 识别的知识缺口 |
| `GapAnalysisResult` | 类 | `scripts.knowledge_gap_identifier` | 缺口分析结果 |
| `GapIdentifierConfig` | 类 | `scripts.knowledge_gap_identifier` | 缺口识别器配置 |
| `KnowledgeGapIdentifier` | 类 | `scripts.knowledge_gap_identifier` | 知识缺口识别器 |
| `create_gap_identifier` | 函数 | `scripts.knowledge_gap_identifier` | 创建知识缺口识别器 |
| `LongTermMemoryManager` | 类 | `scripts.long_term` | 长期记忆管理器 |
| `ConflictCategory` | 枚举 | `scripts.memory_conflict` | 冲突类别 |
| `ConflictAction` | 枚举 | `scripts.memory_conflict` | 冲突处理动作 |
| `SemanticConflict` | 类 | `scripts.memory_conflict` | 语义冲突 |
| `ConflictLogEntry` | 类 | `scripts.memory_conflict` | 冲突日志条目 |
| `ConflictStats` | 类 | `scripts.memory_conflict` | 冲突统计 |
| `ConflictDetectorConfig` | 类 | `scripts.memory_conflict` | 冲突检测器配置 |
| `MemoryConflictDetector` | 类 | `scripts.memory_conflict` | 记忆冲突检测器 |
| `create_memory_conflict_detector` | 函数 | `scripts.memory_conflict` | 创建记忆冲突检测器 |
| `MemoryImportance` | 枚举 | `scripts.memory_forgetting_mechanism` | 记忆重要性 |
| `ForgettingTrigger` | 枚举 | `scripts.memory_forgetting_mechanism` | 遗忘触发因素 |
| `ForgettingAction` | 枚举 | `scripts.memory_forgetting_mechanism` | 遗忘动作 |
| `MemoryState` | 枚举 | `scripts.memory_forgetting_mechanism` | 记忆状态 |
| `MemoryMetadata` | 类 | `scripts.memory_forgetting_mechanism` | 记忆元数据 |
| `ForgettingCandidate` | 类 | `scripts.memory_forgetting_mechanism` | 遗忘候选 |
| `ForgettingDecision` | 类 | `scripts.memory_forgetting_mechanism` | 遗忘决策 |
| `ForgettingReport` | 类 | `scripts.memory_forgetting_mechanism` | 遗忘报告 |
| `ForgettingConfig` | 类 | `scripts.memory_forgetting_mechanism` | 遗忘机制配置 |
| `MemoryForgettingMechanism` | 类 | `scripts.memory_forgetting_mechanism` | 记忆遗忘机制 |
| `create_forgetting_mechanism` | 函数 | `scripts.memory_forgetting_mechanism` | 创建记忆遗忘机制 |
| `TextProcessor` | 类 | `scripts.memory_index` | 文本处理器 |
| `MemoryIndexer` | 类 | `scripts.memory_index` | 记忆索引器 |
| `MemoryDocument` | 类 | `scripts.memory_index` | 记忆文档（用于索引） |
| `SearchResult` | 类 | `scripts.memory_index` | 检索结果 |
| `IndexStats` | 类 | `scripts.memory_index` | 索引统计 |
| `STOPWORDS` | - | `unknown` | Build an unordered collection of unique elements. |
| `MIN_KEYWORD_LENGTH` | 常量 | `unknown` | int([x]) -> integer |
| `SourceType` | 枚举 | `scripts.multi_source_coordinator` | 九类上下文来源 |
| `ConflictType` | 枚举 | `scripts.multi_source_coordinator` | 来源冲突类型 |
| `ResolutionStrategy` | 枚举 | `scripts.multi_source_coordinator` | 冲突解决策略 |
| `SourcePriority` | 类 | `scripts.multi_source_coordinator` | 来源优先级配置 |
| `SourceContent` | 类 | `scripts.multi_source_coordinator` | 来源内容 |
| `ConflictRecord` | 类 | `scripts.multi_source_coordinator` | 冲突记录 |
| `CoordinatorConfig` | 类 | `scripts.multi_source_coordinator` | 协调器配置 |
| `CoordinatedContext` | 类 | `scripts.multi_source_coordinator` | 协调后的上下文 |
| `MultiSourceCoordinator` | 类 | `scripts.multi_source_coordinator` | 多源协调器 |
| `create_coordinator` | 函数 | `scripts.multi_source_coordinator` | 创建多源协调器 |
| `FilterReason` | 枚举 | `scripts.noise_filter` | 过滤原因 |
| `ContentType` | 枚举 | `scripts.noise_filter` | 内容类型 |
| `FilterStrategy` | 枚举 | `scripts.noise_filter` | 过滤策略 |
| `FilterableItem` | 类 | `scripts.noise_filter` | 可过滤项 |
| `FilterResult` | 类 | `scripts.noise_filter` | 过滤结果 |
| `NoiseFilterConfig` | 类 | `scripts.noise_filter` | 噪声过滤器配置 |
| `NoiseFilter` | 类 | `scripts.noise_filter` | 噪声过滤器 |
| `create_noise_filter` | 函数 | `scripts.noise_filter` | 创建噪声过滤器 |
| `MetricType` | 枚举 | `scripts.observability_manager` | 指标类型 |
| `AlertLevel` | 枚举 | `scripts.observability_manager` | 告警级别 |
| `MetricCategory` | 枚举 | `scripts.observability_manager` | 指标类别 |
| `MetricPoint` | 类 | `scripts.observability_manager` | 指标数据点 |
| `TokenUsage` | 类 | `scripts.observability_manager` | Token 使用记录 |
| `LatencyRecord` | 类 | `scripts.observability_manager` | 延迟记录 |
| `QualityMetrics` | 类 | `scripts.observability_manager` | 质量指标 |
| `Alert` | 类 | `scripts.observability_manager` | 告警 |
| `AlertRule` | 类 | `scripts.observability_manager` | 告警规则 |
| `ObservabilityConfig` | 类 | `scripts.observability_manager` | 可观测性配置 |
| `ObservabilityStats` | 类 | `scripts.observability_manager` | 可观测性统计 |
| `ObservabilityManager` | 类 | `scripts.observability_manager` | 可观测性管理器 |
| `LatencyTracker` | 类 | `scripts.observability_manager` | 延迟追踪上下文管理器 |
| `create_observability_manager` | 函数 | `scripts.observability_manager` | 创建可观测性管理器 |
| `PerceptionMemoryStore` | 类 | `scripts.perception` | 感知记忆存储 |
| `PermissionLevel` | 枚举 | `scripts.permission_boundary_controller` | 权限级别 |
| `AccessAction` | 枚举 | `scripts.permission_boundary_controller` | 访问动作 |
| `DataCategory` | 枚举 | `scripts.permission_boundary_controller` | 数据类别 |
| `SensitiveType` | 枚举 | `scripts.permission_boundary_controller` | 敏感信息类型 |
| `FilterAction` | 枚举 | `scripts.permission_boundary_controller` | 过滤动作 |
| `Permission` | 类 | `scripts.permission_boundary_controller` | 权限定义 |
| `Role` | 类 | `scripts.permission_boundary_controller` | 角色定义 |
| `UserPermission` | 类 | `scripts.permission_boundary_controller` | 用户权限 |
| `SensitivePattern` | 类 | `scripts.permission_boundary_controller` | 敏感信息模式 |
| `FilterResult` | 类 | `scripts.permission_boundary_controller` | 过滤结果 |
| `AccessCheckResult` | 类 | `scripts.permission_boundary_controller` | 访问检查结果 |
| `PermissionConfig` | 类 | `scripts.permission_boundary_controller` | 权限控制器配置 |
| `AuditLog` | 类 | `scripts.permission_boundary_controller` | 审计日志 |
| `PermissionBoundaryController` | 类 | `scripts.permission_boundary_controller` | 权限边界控制器 |
| `create_permission_controller` | 函数 | `scripts.permission_boundary_controller` | 创建权限边界控制器 |
| `ConsentStatus` | 枚举 | `scripts.privacy` | 同意状态 |
| `DataSensitivity` | 枚举 | `scripts.privacy` | 数据敏感度级别 |
| `StoragePolicy` | 枚举 | `scripts.privacy` | 存储策略 |
| `RetentionPeriod` | 枚举 | `scripts.privacy` | 保留期限 |
| `ConsentRecord` | 类 | `scripts.privacy` | 同意记录 |
| `PrivacyConfig` | 类 | `scripts.privacy` | 隐私配置 |
| `DataClassification` | 类 | `scripts.privacy` | 数据分类结果 |
| `PrivacyAuditLog` | 类 | `scripts.privacy` | 隐私审计日志 |
| `SensitiveDataDetector` | 类 | `scripts.privacy` | 敏感数据检测器 |
| `PrivacyManager` | 类 | `scripts.privacy` | 隐私管理器 |
| `PRIVACY_NOTICE_TEMPLATE` | 常量 | `unknown` | str(object='') -> str |
| `OptimizedDualTrackProcessor` | 类 | `scripts.processors.optimized_dual_track_processor` | 优化的双轨处理器 |
| `ProcessingResult` | 类 | `scripts.processors.optimized_dual_track_processor` | 处理结果 |
| `ChainCacheManager` | 类 | `scripts.processors.chain_cache_manager` | 链缓存管理器 |
| `ChainCacheEntry` | 类 | `scripts.processors.chain_cache_manager` | 链缓存条目 |
| `MonitoringSystem` | 类 | `scripts.processors.monitoring_system` | 监控系统 |
| `Metric` | 类 | `scripts.processors.monitoring_system` | 指标 |
| `HealthCheck` | 类 | `scripts.processors.monitoring_system` | 健康检查结果 |
| `DualTrackIntegrationAdapter` | 类 | `scripts.processors.dual_track_integration_adapter` | 双轨集成适配器 |
| `REDIS_AVAILABLE` | 常量 | `unknown` | Returns True when the argument is true, False otherwise. |
| `RedisConfig` | 类 | `scripts.redis_adapter` | Redis 连接配置（安全增强版） |
| `RedisKeyBuilder` | 类 | `scripts.redis_adapter` | Redis Key 命名工具 |
| `RedisAdapter` | 类 | `scripts.redis_adapter` | Redis 适配器 |
| `create_redis_adapter` | 函数 | `scripts.redis_adapter` | 创建 Redis 适配器 |
| `ContentType` | 枚举 | `scripts.result_compressor` | 内容类型 |
| `ErrorSeverity` | 枚举 | `scripts.result_compressor` | 错误严重程度 |
| `CompressionStrategy` | 枚举 | `scripts.result_compressor` | 压缩策略 |
| `ErrorInfo` | 类 | `scripts.result_compressor` | 错误信息 |
| `WarningInfo` | 类 | `scripts.result_compressor` | 警告信息 |
| `CausalChain` | 类 | `scripts.result_compressor` | 因果链 |
| `DecisionPoint` | 类 | `scripts.result_compressor` | 决策点 |
| `CompressedResult` | 类 | `scripts.result_compressor` | 压缩结果 |
| `CompressionConfig` | 类 | `scripts.result_compressor` | 压缩配置 |
| `ResultCompressor` | 类 | `scripts.result_compressor` | 结果压缩器 |
| `create_result_compressor` | 函数 | `scripts.result_compressor` | 创建结果压缩器 |
| `RetrievalNeed` | 枚举 | `scripts.retrieval_decision_engine` | 检索需求级别 |
| `QueryType` | 枚举 | `scripts.retrieval_decision_engine` | 查询类型 |
| `RetrievalStrategy` | 枚举 | `scripts.retrieval_decision_engine` | 检索策略 |
| `CacheDecision` | 枚举 | `scripts.retrieval_decision_engine` | 缓存决策 |
| `QueryAnalysis` | 类 | `scripts.retrieval_decision_engine` | 查询分析结果 |
| `CacheStatus` | 类 | `scripts.retrieval_decision_engine` | 缓存状态 |
| `RetrievalDecision` | 类 | `scripts.retrieval_decision_engine` | 检索决策 |
| `DecisionConfig` | 类 | `scripts.retrieval_decision_engine` | 决策配置 |
| `RetrievalDecisionEngine` | 类 | `scripts.retrieval_decision_engine` | 检索时机决策引擎 |
| `create_retrieval_decision_engine` | 函数 | `scripts.retrieval_decision_engine` | 创建检索决策引擎 |
| `RelevanceSource` | 枚举 | `scripts.retrieval_organizer` | 相关性来源 |
| `DiversityStrategy` | 枚举 | `scripts.retrieval_organizer` | 多样性策略 |
| `RerankStrategy` | 枚举 | `scripts.retrieval_organizer` | 重排序策略 |
| `RetrievalItem` | 类 | `scripts.retrieval_organizer` | 检索项 |
| `RerankedItem` | 类 | `scripts.retrieval_organizer` | 重排序后的项 |
| `RetrievalOrganizerConfig` | 类 | `scripts.retrieval_organizer` | 检索组织器配置 |
| `OrganizedRetrieval` | 类 | `scripts.retrieval_organizer` | 组织后的检索结果 |
| `RetrievalOrganizer` | 类 | `scripts.retrieval_organizer` | 检索结果组织器 |
| `create_retrieval_organizer` | 函数 | `scripts.retrieval_organizer` | 创建检索结果组织器 |
| `QualityDimension` | 枚举 | `scripts.retrieval_quality_evaluator` | 质量维度 |
| `QualityLevel` | 枚举 | `scripts.retrieval_quality_evaluator` | 质量级别 |
| `ReretrievalNeed` | 枚举 | `scripts.retrieval_quality_evaluator` | 二次检索需求 |
| `RetrievalItem` | 类 | `scripts.retrieval_quality_evaluator` | 检索项 |
| `DimensionScore` | 类 | `scripts.retrieval_quality_evaluator` | 维度评分 |
| `QualityAssessment` | 类 | `scripts.retrieval_quality_evaluator` | 质量评估结果 |
| `ReretrievalDecision` | 类 | `scripts.retrieval_quality_evaluator` | 二次检索决策 |
| `EvaluationResult` | 类 | `scripts.retrieval_quality_evaluator` | 评估结果 |
| `EvaluatorConfig` | 类 | `scripts.retrieval_quality_evaluator` | 评估器配置 |
| `RetrievalQualityEvaluator` | 类 | `scripts.retrieval_quality_evaluator` | 检索质量评估器 |
| `create_quality_evaluator` | 函数 | `scripts.retrieval_quality_evaluator` | 创建质量评估器 |
| `SemanticBucket` | 类 | `scripts.short_term` | 语义分类桶 |
| `ShortTermMemoryManager` | 类 | `scripts.short_term` | 短期记忆管理器 |
| `AsynchronousExtractor` | 类 | `scripts.short_term` | 异步提炼器（洞察驱动版） |
| `TopicCluster` | 类 | `scripts.short_term_insight` | 话题簇 |
| `TopicRelation` | 类 | `scripts.short_term_insight` | 话题关联 |
| `ExtractionDecision` | 类 | `scripts.short_term_insight` | 提炼决策 |
| `ShortTermInsightResult` | 类 | `scripts.short_term_insight` | 短期洞察结果 |
| `ShortTermInsightAnalyzer` | 类 | `scripts.short_term_insight` | 短期记忆洞察分析器 |
| `ShortTermMemoryItemRedis` | 类 | `scripts.short_term_redis` | 短期记忆项（Redis 存储格式） |
| `ShortTermRedisConfig` | 类 | `scripts.short_term_redis` | 短期记忆 Redis 配置 |
| `ShortTermMemoryRedis` | 类 | `scripts.short_term_redis` | 短期记忆 Redis 存储 |
| `create_short_term_redis` | 函数 | `scripts.short_term_redis` | 创建短期记忆 Redis 存储 |
| `ConsistencyLevel` | 枚举 | `scripts.state_consistency_validator` | 一致性级别 |
| `ConflictSeverity` | 枚举 | `scripts.type_defs` | 冲突严重程度 |
| `ResolutionStrategy` | 枚举 | `scripts.state_consistency_validator` | 解决策略 |
| `StateModule` | 枚举 | `scripts.state_consistency_validator` | 状态模块 |
| `StateSnapshot` | 类 | `scripts.state_consistency_validator` | 状态快照 |
| `StateConflict` | 类 | `scripts.state_consistency_validator` | 状态冲突 |
| `ConsistencyReport` | 类 | `scripts.state_consistency_validator` | 一致性报告 |
| `ValidatorConfig` | 类 | `scripts.state_consistency_validator` | 校验器配置 |
| `StateConsistencyValidator` | 类 | `scripts.state_consistency_validator` | 状态一致性校验器 |
| `create_state_validator` | 函数 | `scripts.state_consistency_validator` | 创建状态一致性校验器 |
| `InferenceType` | 枚举 | `scripts.state_inference_engine` | 推理类型 |
| `InferenceConfidence` | 枚举 | `scripts.state_inference_engine` | 推理置信度 |
| `InferenceSource` | 枚举 | `scripts.state_inference_engine` | 推理来源 |
| `InferencePremise` | 类 | `scripts.state_inference_engine` | 推理前提 |
| `InferenceRule` | 类 | `scripts.state_inference_engine` | 推理规则 |
| `InferenceResult` | 类 | `scripts.state_inference_engine` | 推理结果 |
| `StateTransition` | 类 | `scripts.state_inference_engine` | 状态转移 |
| `TransitionGraph` | 类 | `scripts.state_inference_engine` | 状态转移图 |
| `InferenceEngineConfig` | 类 | `scripts.state_inference_engine` | 推理引擎配置 |
| `StateInferenceEngine` | 类 | `scripts.state_inference_engine` | 状态推理引擎 |
| `create_inference_engine` | 函数 | `scripts.state_inference_engine` | 创建状态推理引擎 |
| `StepStatus` | 枚举 | `scripts.task_progress` | 步骤状态 |
| `StepType` | 枚举 | `scripts.task_progress` | 步骤类型 |
| `GoalStatus` | 枚举 | `scripts.task_progress` | 目标状态 |
| `AlignmentLevel` | 枚举 | `scripts.task_progress` | 对齐程度 |
| `TaskStep` | 类 | `scripts.task_progress` | 任务步骤 |
| `TaskGoal` | 类 | `scripts.task_progress` | 任务目标 |
| `StepDependency` | 类 | `scripts.task_progress` | 步骤依赖关系 |
| `ProgressReport` | 类 | `scripts.task_progress` | 进度报告 |
| `GoalAlignmentCheck` | 类 | `scripts.task_progress` | 目标对齐检查结果 |
| `TaskProgressConfig` | 类 | `scripts.task_progress` | 任务进度配置 |
| `TaskProgressTracker` | 类 | `scripts.task_progress` | 任务进度追踪器 |
| `create_task_progress_tracker` | 函数 | `scripts.task_progress` | 创建任务进度追踪器 |
| `TokenType` | 枚举 | `scripts.token_budget` | Token 类型 |
| `BudgetPolicy` | 枚举 | `scripts.token_budget` | 预算策略 |
| `TokenBudgetConfig` | 类 | `scripts.token_budget` | Token 预算配置 |
| `TokenCounter` | 类 | `scripts.token_budget` | Token 计数器 |
| `TokenBudgetManager` | 类 | `scripts.token_budget` | Token 预算管理器 |
| `create_token_budget_manager` | 函数 | `scripts.token_budget` | 创建 Token 预算管理器 |
| `CoordinatedExtractionTrigger` | 类 | `scripts.triggers.coordinated_extraction_trigger` | 协同提取触发器 |
| `ExtractionAction` | 类 | `scripts.triggers.coordinated_extraction_trigger` | 提取动作 |
| `MemoryType` | 枚举 | `scripts.type_defs` | 记忆类型枚举 |
| `MemoryCategory` | 枚举 | `scripts.type_defs` | 8种记忆分类体系 |
| `SemanticBucketType` | 枚举 | `scripts.type_defs` | 语义分类桶类型 |
| `QualityDimension` | 枚举 | `scripts.type_defs` | 六维质量评估维度 |
| `ScenarioType` | 枚举 | `scripts.type_defs` | 场景类型 |
| `PhaseType` | 枚举 | `scripts.type_defs` | 阶段类型 |
| `UserStateType` | 枚举 | `scripts.type_defs` | 用户状态类型 |
| `HeatLevel` | 枚举 | `scripts.type_defs` | 冷热度层级 |
| `ConflictType` | 枚举 | `scripts.type_defs` | 冲突类型 |
| `ResolutionMode` | 枚举 | `scripts.type_defs` | 冲突解决模式 |
| `TriggerDimension` | 枚举 | `scripts.type_defs` | 激活器维度 |
| `SignalType` | 枚举 | `scripts.type_defs` | 洞察信号类型 |
| `InsightType` | 枚举 | `scripts.type_defs` | 洞察类型 |
| `InsightPriority` | 枚举 | `scripts.type_defs` | 洞察优先级 |
| `SignalStrength` | 枚举 | `scripts.type_defs` | 信号强度 |
| `DecisionType` | 枚举 | `scripts.type_defs` | 决策类型 |
| `TaskType` | 枚举 | `scripts.type_defs` | 任务类型 |
| `ConflictSeverity` | 枚举 | `scripts.type_defs` | 冲突严重程度 |
| `ReflectionTriggerType` | 枚举 | `scripts.type_defs` | 反思触发类型 |
| `ReflectionOutcome` | 枚举 | `scripts.type_defs` | 反思结果类型（元学习标签） |
| `LearningValue` | 枚举 | `scripts.type_defs` | 元学习价值评估 |
| `ReflectionSeverity` | 枚举 | `scripts.type_defs` | 反思问题严重程度 |
| `ReflectionSignal` | 类 | `scripts.type_defs` | 模型自检测的反思信号（嵌入推理输出中） |
| `ReasoningStepWithReflection` | 类 | `scripts.type_defs` | 带反思信号的推理步骤 |
| `ReflectionTriggerRecord` | 类 | `scripts.type_defs` | 反思触发记录（存储到短期记忆） |
| `ReflectionProcessResult` | 类 | `scripts.type_defs` | 反思执行结果 |
| `VerificationResult` | 类 | `scripts.type_defs` | 验证结果 |
| `ReflectionMemoryItem` | 类 | `scripts.type_defs` | 反思记忆项（持久化到长期记忆） |
| `MetaLearningSample` | 类 | `scripts.type_defs` | 元学习训练样本 |
| `ExtractionMapping` | 类 | `scripts.type_defs` | 提炼映射工具 |
| `TimestampMixin` | 类 | `scripts.type_defs` | 时间戳混入 |
| `ConfidenceMixin` | 类 | `scripts.type_defs` | 置信度混入 |
| `HeatMixin` | 类 | `scripts.type_defs` | 热度混入 |
| `ShortTermMemoryItem` | 类 | `scripts.type_defs` | 短期记忆项 |
| `ShortTermMemoryBucket` | 类 | `scripts.type_defs` | 短期记忆语义分类桶 |
| `ExtractionTrigger` | 类 | `scripts.type_defs` | 提炼触发条件 |
| `QualityScores` | 类 | `scripts.type_defs` | 六维质量分数 |
| `WeightConfig` | 类 | `scripts.type_defs` | 权重配置 |
| `ContextPackage` | 类 | `scripts.type_defs` | 上下文包 |
| `TechnicalBackground` | 类 | `scripts.type_defs` | 技术背景 |
| `CommunicationStyle` | 类 | `scripts.type_defs` | 沟通风格 |
| `DecisionPattern` | 类 | `scripts.type_defs` | 决策模式 |
| `UserProfileData` | 类 | `scripts.type_defs` | 用户画像数据 |
| `UserProfileMemory` | 类 | `scripts.type_defs` | 用户画像记忆 |
| `DecisionPatternRecord` | 类 | `scripts.type_defs` | 决策模式记录 |
| `ProblemSolvingStrategy` | 类 | `scripts.type_defs` | 问题解决策略 |
| `ToolUsageRecord` | 类 | `scripts.type_defs` | 工具使用记录 |
| `ToolOptimalContext` | 类 | `scripts.type_defs` | 工具最优场景 |
| `ToolCombinationPattern` | 类 | `scripts.type_defs` | 工具组合模式 |
| `NeuroticismTendency` | 类 | `scripts.type_defs` | 神经质倾向 |
| `ProceduralMemoryData` | 类 | `scripts.type_defs` | 程序性记忆数据 |
| `ProceduralMemory` | 类 | `scripts.type_defs` | 程序性记忆 |
| `GrowthMilestone` | 类 | `scripts.type_defs` | 成长节点 |
| `IdentityEvolution` | 类 | `scripts.type_defs` | 身份演化 |
| `NarrativeMemoryData` | 类 | `scripts.type_defs` | 叙事记忆数据 |
| `NarrativeMemory` | 类 | `scripts.type_defs` | 叙事记忆 |
| `ConceptDefinition` | 类 | `scripts.type_defs` | 概念定义 |
| `KnowledgeEntity` | 类 | `scripts.type_defs` | 知识实体 |
| `Principle` | 类 | `scripts.type_defs` | 原则 |
| `SemanticMemoryData` | 类 | `scripts.type_defs` | 语义记忆数据 |
| `SemanticMemory` | 类 | `scripts.type_defs` | 语义记忆 |
| `EmotionState` | 类 | `scripts.type_defs` | 情绪状态 |
| `AttitudeTendency` | 类 | `scripts.type_defs` | 态度倾向 |
| `SatisfactionRecord` | 类 | `scripts.type_defs` | 满意度记录 |
| `EmotionalMemoryData` | 类 | `scripts.type_defs` | 情感记忆数据 |
| `EmotionalMemory` | 类 | `scripts.type_defs` | 情感记忆 |
| `ConversationTurn` | 类 | `scripts.type_defs` | 对话轮次 |
| `TaskState` | 类 | `scripts.type_defs` | 任务状态 |
| `TemporaryContext` | 类 | `scripts.type_defs` | 临时上下文 |
| `PerceptionMemoryData` | 类 | `scripts.type_defs` | 感知记忆数据 |
| `PerceptionMemory` | 类 | `scripts.type_defs` | 感知记忆 |
| `CurrentTask` | 类 | `scripts.type_defs` | 当前任务 |
| `UserCurrentState` | 类 | `scripts.type_defs` | 用户当前状态 |
| `ContextAnchors` | 类 | `scripts.type_defs` | 上下文锚点 |
| `SituationAwareness` | 类 | `scripts.type_defs` | 情境感知 |
| `ActivationSource` | 类 | `scripts.type_defs` | 激活来源 |
| `ActivatedMemory` | 类 | `scripts.type_defs` | 激活的记忆 |
| `ActivationResult` | 类 | `scripts.type_defs` | 激活结果 |
| `TaskContextLayer` | 类 | `scripts.type_defs` | 任务上下文层 |
| `UserStateLayer` | 类 | `scripts.type_defs` | 用户状态层 |
| `ActivatedExperiencesLayer` | 类 | `scripts.type_defs` | 激活经验层 |
| `KnowledgeContextLayer` | 类 | `scripts.type_defs` | 知识上下文层 |
| `EmotionalContextLayer` | 类 | `scripts.type_defs` | 情感上下文层 |
| `NarrativeAnchorLayer` | 类 | `scripts.type_defs` | 叙事锚点层 |
| `ReconstructedContext` | 类 | `scripts.type_defs` | 重构上下文 |
| `FitScores` | 类 | `scripts.type_defs` | 契合度分数 |
| `DecisionSupportSignal` | 类 | `scripts.type_defs` | 决策支持信号 |
| `ToolRecommendationSignal` | 类 | `scripts.type_defs` | 工具推荐信号 |
| `RiskAlertSignal` | 类 | `scripts.type_defs` | 风险提示信号 |
| `TimingHintSignal` | 类 | `scripts.type_defs` | 时机提示信号 |
| `InsightSignalUnion` | 类 | `scripts.type_defs` | 洞察信号联合类型 |
| `ContextEnhancement` | 类 | `scripts.type_defs` | 上下文增强 |
| `InsightSignal` | 类 | `scripts.type_defs` | 洞察信号 |
| `Insight` | 类 | `scripts.type_defs` | 洞察 |
| `InsightPoolData` | 类 | `scripts.type_defs` | 洞察池数据 |
| `UserDecision` | 类 | `scripts.type_defs` | 用户决策 |
| `StateEventType` | 枚举 | `scripts.type_defs` | 状态事件类型 |
| `CheckpointRecord` | 类 | `scripts.type_defs` | 检查点记录 |
| `StateChangeEvent` | 类 | `scripts.type_defs` | 状态变化事件 |
| `StateSubscription` | 类 | `scripts.type_defs` | 状态订阅配置 |
| `MemoryConflict` | 类 | `scripts.type_defs` | 记忆冲突 |
| `ConflictResolution` | 类 | `scripts.type_defs` | 冲突解决结果 |
| `MemoryConflictExtended` | 类 | `scripts.type_defs` | 扩展的记忆冲突 |
| `ResolutionResult` | 类 | `scripts.type_defs` | 解决结果 |
| `ModuleState` | 类 | `scripts.type_defs` | 模块状态 |
| `GlobalState` | 类 | `scripts.type_defs` | 全局状态 |
| `AsyncTask` | 类 | `scripts.type_defs` | 异步任务 |
| `GlobalStateSnapshot` | 类 | `scripts.type_defs` | 全局状态快照 |
| `SceneContext` | 类 | `scripts.type_defs` | 场景上下文 |
| `LongTermMemoryContainer` | 类 | `scripts.type_defs` | 长期记忆统一容器 |