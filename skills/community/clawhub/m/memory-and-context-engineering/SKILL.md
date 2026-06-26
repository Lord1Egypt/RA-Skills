---
name: agent-memory
description: 用户与模型间的任何交互行为都会触发此技能；提供Context Engineering五大核心能力（选择、压缩、检索、状态、记忆）及认知模型层支持；作为元技能强制常驻运行
always: true
dependency:
  python:
    - pydantic>=2.0.0
    - typing-extensions>=4.0.0
    - cryptography>=41.0.0
    - redis>=4.5.0
    - tiktoken>=0.5.0
    - mmh3>=3.0.0
license: GPL-3.0
author: kiwifruit
---

# Agent Memory System

**版权所有 © 2024 kiwifruit**

本程序采用 GNU General Public License v3.0 许可证。

详见: [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html)

## 任务目标

- 本 Skill 用于：为智能体构建完整的记忆能力基础设施，实现 Context Engineering 核心能力
- 触发条件：**元技能，强制常驻运行**（`always: true`）
- 核心能力：
  - **选择**：噪声过滤 + 相关性筛选
  - **压缩**：链结构提取（因果/逻辑/操作/叙事/时间）+ 工具结果压缩
  - **检索**：结果重排序 + 多样性保证
  - **状态**：任务进度追踪 + 目标对齐
  - **记忆**：冲突检测 + 跨会话关联

### 架构概述

本 Skill 采用**四层架构**（新），以认知模型层为核心，**ContextOrchestrator 为统一入口和总控中心**：

```
┌─────────────────────────────────────────────────────────────────┐
│                  顶层：总控层（统一入口）                         │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │           ContextOrchestrator（总控中心）                   │  │
│  │  • Token预算管理  • 检索决策  • 多源协调  • 结果压缩        │  │
│  │  • 认知模型构建  • 全局调度  • 可观测性管理                │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  中间层：协调层                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │           认知模型层（核心业务逻辑）                       │  │
│  │  • CognitiveModelBuilder  • CausalChainExtractor          │  │
│  │  • KnowledgeGapIdentifier • RetrievalDecisionEngine       │  │
│  │  • ...（其他5个组件）                                    │  │
│  └───────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │        双轨架构（认知模型的具体实现层）                    │  │
│  │  • 轨道A：语义桶提炼  • 轨道B：链提取  • 融合层          │  │
│  │  • 5种链类型：因果/逻辑/操作/叙事/时间                    │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  基础层：存储层                                 │
│  • ShortTermMemory  • LongTermMemory  • MemoryIndexer          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  底层：基础设施层                               │
│  • type_defs  • encryption  • privacy  • monitoring            │
└─────────────────────────────────────────────────────────────────┘
```

**ContextOrchestrator 是系统的总控中心和统一入口**（顶层），负责：
- Token 预算管理
- 检索决策
- 多源协调（认知模型、双轨、存储层）
- 结果压缩
- 全局调度

**认知模型层是协调层的核心**（中间层），负责：
- 认知模型构建
- 链提取（5种）
- 知识缺口识别
- 检索决策
- 状态推理

**双轨架构是协调层的子层**（中间层），为认知模型层提供技术实现：
- 轨道A：语义桶提炼
- 轨道B：链提取（因果/逻辑/操作/叙事/时间）
- 融合层：关联、验证、摘要

详见：[架构总览](references/architecture_overview.md)、[双轨架构总览](references/dual_track_architecture_overview.md)

## 前置准备

### 依赖安装

```bash
pip install pydantic>=2.0.0 typing-extensions>=4.0.0 cryptography>=41.0.0 redis>=4.5.0 tiktoken>=0.5.0 mmh3>=3.0.0
```

### 存储路径配置

所有模块初始化时**必须指定存储路径**：

```python
base_path = "./memory_data"
key_storage_path = f"{base_path}/keys"
sync_state_path = f"{base_path}/sync_state"
index_storage_path = f"{base_path}/memory_index"
credential_path = f"{base_path}/credentials"
```

### Redis 连接（可选，推荐）

```python
from scripts import create_redis_adapter

redis_adapter = create_redis_adapter(host="localhost", port=6379)
if redis_adapter.is_available():
    print("Redis 连接成功")
```

## 核心流程

### 1. 隐私配置（必需）

```python
from scripts import PrivacyManager, ConsentStatus

privacy_manager = PrivacyManager(user_id="user_123")

# 检查隐私同意状态
status = privacy_manager.get_consent_status("memory_storage")

if status != ConsentStatus.GRANTED:
    # 创建同意请求（返回 PENDING 状态的记录）
    record = privacy_manager.request_consent(
        consent_type="memory_storage",
        description="是否允许存储交互记忆？"
    )

    # 智能体负责向用户呈现描述信息并获取同意
    # 例如：向用户展示 "是否允许存储交互记忆？"
    # 如果用户同意，调用以下方法授予同意：
    # privacy_manager.grant_consent(record.consent_id)

    # 注意：request_consent() 不会弹窗，智能体需要负责与用户交互
```

### 2. 初始化核心模块

```python
from scripts import (
    PerceptionMemoryStore,
    ShortTermMemoryManager,
    LongTermMemoryManager,
    ContextReconstructor,
)

perception = PerceptionMemoryStore()
short_term = ShortTermMemoryManager()
long_term = LongTermMemoryManager()
reconstructor = ContextReconstructor()
```

### 3. 处理对话

```python
# 创建会话
session_id = perception.create_session()
perception.store_conversation(session_id, user_message, system_response)

# 短期记忆
from scripts import SemanticBucketType
short_term.store_with_semantics(
    user_message,
    SemanticBucketType.USER_INTENT,
    "话题",
    0.8
)
```

### 4. 上下文重构

```python
context = reconstructor.reconstruct(situation, long_term.get_all_memories())
```

### 5. 使用统一入口（推荐）

```python
from scripts import create_context_orchestrator

orchestrator = create_context_orchestrator(
    user_id="user_123",
    session_id="session_456",
    max_context_tokens=32000,
)

# 准备上下文
prepared = orchestrator.prepare_context(
    user_input="用户输入",
    system_instruction="系统指令",
)
```

> **重要说明**：`ContextOrchestrator` 是系统的**总控中心和统一入口**（顶层），负责协调所有层级的执行。推荐始终使用 `ContextOrchestrator` 而非直接调用内部模块。

## 高级功能

### 上下文压缩

本系统提供完整的上下文压缩能力，支持 5 种压缩策略和自动压缩。

```python
# 启用上下文压缩
orchestrator.enable_context_compression(
    enable_auto_compress=True,
    auto_compress_threshold=0.8,
    default_strategy="priority_based",
)

# 手动压缩
compressed_blocks = orchestrator.compress_context(
    blocks=blocks,
    compression_ratio=0.7,
    strategy="priority_based"
)
```

详细说明：[上下文压缩 API](references/api_reference.md#上下文压缩-api)、[压缩规则](references/context_compaction_rules.md)

### 质量评估与监控

本系统提供完整的 metadata 质量评估、自定义类型生命周期管理和使用监控能力。

```python
# 启用质量评估
orchestrator.enable_quality_assessment(
    storage_path="usage_stats.json",
    enable_monitoring=True,
)

# 评估 metadata 质量
assessment = orchestrator.assess_metadata_quality(metadata, ContextSource.CUSTOM)
print(f"质量评分: {assessment.score}")
```

详细说明：[质量评估与监控 API](references/api_reference.md#质量评估与监控-api)

### 上下文类型扩展

本系统支持通过 **混合方案** 处理已知和未知类型的上下文信息：
- **已知类型**：使用标准来源 + `subtype` 字段
- **未知类型**：使用 `CUSTOM` 来源 + `custom_type` 字段

```python
# 注册自定义类型
orchestrator.register_custom_type(
    custom_type="workflow_step",
    priority=ContextPriority.HIGH,
    required_fields=["step_id", "status"]
)
```

详细说明：[上下文类型扩展](references/architecture_overview.md#十七上下文类型扩展混合方案)

### 错误处理与纠正机制

本系统内置错误处理和纠正机制，支持 Agent 工具调用的可靠性规范。

详细说明：[工具调用可靠性规则](references/agent_tools_use_rules.md)

## 注意事项

1. **路径必传**：所有存储路径无默认值，必须显式传入
2. **隐私优先**：处理用户数据前必须初始化 `PrivacyManager` 并获取同意
3. **敏感数据**：系统自动识别密码、账号等敏感信息，默认不存储
4. **类型安全**：所有函数必须有类型注解，禁止使用裸 dict
5. **异步优先**：提炼、热度计算等后台异步执行
6. **降级策略**：模块故障时自动降级，保证核心流程可用
7. **统一入口**：推荐使用 `ContextOrchestrator` 作为统一入口，避免直接调用内部模块
8. **Skill 定位**：本 Skill 是能力扩展包，由智能体动态加载，非独立应用
9. **隐私同意流程**：`request_consent()` 不会弹窗，智能体需要负责向用户呈现描述信息并调用 `grant_consent()` 授予同意

## 常见问题

### Q: 如何选择存储方案？

**A**:
- **文件存储**：默认方案，适合大多数场景，无需额外依赖
- **Redis 存储**：高性能场景，需要部署 Redis 服务器

### Q: 如何优化 Token 使用？

**A**: 使用 `ContextOrchestrator` 自动管理 Token 预算，系统会智能压缩和筛选内容。

### Q: 如何处理记忆冲突？

**A**: 系统自动检测和解决冲突，无需手动处理。`ContextOrchestrator` 内置冲突解决机制。

### Q: 如何导出和导入记忆数据？

**A**: 使用 `LongTermMemoryManager` 的 `export()` 和 `import()` 方法。

### Q: 如何监控记忆系统性能？

**A**: 系统内置监控能力，可通过 `ContextOrchestrator` 获取性能统计信息。

### Q: Skill 如何运行？

**A**: 本 Skill 是智能体的能力扩展包，由智能体动态加载和执行。不需要独立启动服务器或监听端口。所有交互通过智能体与用户的对话完成。

详见 [architecture_execution_model.md](references/architecture_execution_model.md)。

## 资源索引

### 参考文档

| 文档 | 用途 | 何时读取 |
|------|------|----------|
| **核心参考** | | |
| [module_index.md](references/module_index.md) | 模块索引 | 查找特定模块和功能（67 个模块完整索引） |
| [usage_guide.md](references/usage_guide.md) | 使用指南 | 学习各模块的详细使用方法 |
| [api_reference.md](references/api_reference.md) | API 参考 | 查询所有公开 API 的详细文档 |
| [best_practices.md](references/best_practices.md) | 最佳实践 | 学习架构设计、性能优化、安全性等最佳实践 |
| [troubleshooting.md](references/troubleshooting.md) | 故障排查 | 解决常见问题和错误 |
| **架构与设计** | | |
| [architecture_overview.md](references/architecture_overview.md) | 架构概览 | 理解整体架构设计理念 |
| [architecture_execution_model.md](references/architecture_execution_model.md) | 执行模型 | 了解 Skill 的执行模型和工作流程 |
| [dual_track_architecture_overview.md](references/dual_track_architecture_overview.md) | 双轨架构总览 | 理解语义桶与链提取的双轨并行架构 |
| [dual_track_module_design.md](references/dual_track_module_design.md) | 双轨模块设计 | 查看双轨架构的数据结构、接口定义、类图和关键算法 |
| [dual_track_implementation_guide.md](references/dual_track_implementation_guide.md) | 双轨实施指南 | 按步骤实施双轨架构的完整指南 |
| **功能参考** | | |
| [context_compaction_rules.md](references/context_compaction_rules.md) | 上下文压缩规则 | 学习压缩规则、错误记忆机制、最佳实践 |
| [chain_aware_compression_stage1.md](references/chain_aware_compression_stage1.md) | 链感知压缩（阶段1） | 学习链元数据增强、链感知压缩策略 |
| [agent_tools_use_rules.md](references/agent_tools_use_rules.md) | 工具调用规范 | 集成外部工具时遵循的规范 |
| **Agent 集成** | | |
| [agent_loops_integration.md](references/agent_loops_integration.md) | Agent 循环集成 | 学习如何将记忆系统集成到 Agent 循环中 |

### 核心模块

本系统包含 **67 个脚本模块**，按四层架构分类为总控层、协调层、存储层、基础设施层。

| 模块 | 路径 | 功能 | 层级 |
|------|------|------|------|
| **总控层** | | | |
| ContextOrchestrator | `scripts/context_orchestrator.py` | 上下文编排器（统一入口、总控中心） | 总控层 |
| TokenBudgetManager | `scripts/token_budget.py` | Token 预算管理 | 总控层 |
| **协调层：认知模型层** | | | |
| CognitiveModelBuilder | `scripts/cognitive_model_builder.py` | 认知模型构建器 | 协调层 |
| CausalChainExtractor | `scripts/causal_chain_extractor.py` | 因果链提取器 | 协调层 |
| KnowledgeGapIdentifier | `scripts/knowledge_gap_identifier.py` | 知识缺口识别器 | 协调层 |
| RetrievalDecisionEngine | `scripts/retrieval_decision_engine.py` | 检索决策引擎 | 协调层 |
| **协调层：双轨架构** | | | |
| BaseExtractedChain | `scripts/chains/base_chain.py` | 链基类 | 协调层 |
| ExtractedCausalChain | `scripts/chains/causal_chain.py` | 因果链 | 协调层 |
| ExtractedLogicChain | `scripts/chains/logic_chain.py` | 逻辑链 | 协调层 |
| ExtractedOperationChain | `scripts/chains/operation_chain.py` | 操作链 | 协调层 |
| ExtractedNarrativeChain | `scripts/chains/narrative_chain.py` | 叙事链 | 协调层 |
| ExtractedTimeChain | `scripts/chains/time_chain.py` | 时间链 | 协调层 |
| ChainBuffer | `scripts/chains/chain_buffer.py` | 链缓冲区 | 协调层 |
| TopicCluster | `scripts/buckets/topic_cluster.py` | 话题簇 | 协调层 |
| BucketChainLinker | `scripts/fusion/bucket_chain_linker.py` | 桶-链关联器 | 协调层 |
| CrossValidator | `scripts/fusion/cross_validator.py` | 交叉验证器 | 协调层 |
| MultiDimensionSummaryGenerator | `scripts/fusion/multi_dimension_summary.py` | 多维摘要生成器 | 协调层 |
| BucketChainFusion | `scripts/fusion/bucket_chain_fusion.py` | 融合层总控 | 协调层 |
| CoordinatedExtractionTrigger | `scripts/triggers/coordinated_extraction_trigger.py` | 协同提取触发器 | 协调层 |
| **存储层** | | | |
| ShortTermMemoryRedis | `scripts/short_term_redis.py` | 短期记忆（Redis） | 存储层 |
| LongTermMemoryManager | `scripts/long_term.py` | 长期记忆管理 | 存储层 |
| MemoryIndexer | `scripts/memory_indexer.py` | 记忆索引 | 存储层 |
| **基础设施层** | | | |
| PrivacyManager | `scripts/privacy.py` | 隐私管理 | 基础设施层 |
| Encryption | `scripts/encryption.py` | 加密解密 | 基础设施层 |
| MonitoringSystem | `scripts/monitoring_system.py` | 监控系统 | 基础设施层 |

> **查看完整模块索引**：详见 [module_index.md](references/module_index.md)（包含所有 67 个模块的详细信息、用途和使用建议）

### 阶段实施总结

本 Skill 采用四层架构，分阶段实施：

- **阶段 1**：基础架构（CUSTOM 枚举值、MetadataValidator、PriorityResolver）
- **阶段 2**：高级功能（自定义类型注册、动态优先级规则、批量解析、缓存机制）
- **阶段 3**：质量评估与生命周期管理（MetadataQualityAssessor、CustomTypeLifecycleManager、UsageMonitor、QualityReportGenerator）
- **阶段 4**：性能优化（LRUCache、PerformanceMonitor、BatchProcessor）
- **阶段 5.1**：上下文压缩（ContextCompressor、CompressionStrategy、/compact 命令、自动压缩）
- **阶段 5.2**：链感知压缩（链元数据增强、CHAIN_AWARE 压缩策略、链类型权重配置）
- **阶段 6**：双轨架构（协调层子层，为认知模型层提供技术实现）
  - 轨道A：语义桶提炼
  - 轨道B：链提取（5种链类型：因果/逻辑/操作/叙事/时间）
  - 融合层：关联、验证、摘要
  - 触发器：协同提取触发
- **阶段 7**：四层架构澄清与文档完善
  - 明确ContextOrchestrator为顶层总控中心和统一入口
  - 明确认知模型层为协调层核心业务逻辑
  - 明确双轨架构为协调层子层，为认知模型层提供技术实现
  - 完善架构总览、API参考文档、双轨架构文档
- **阶段 8**：文档完善（API 参考文档、最佳实践、故障排查指南、上下文压缩规则、链感知压缩文档）

### 性能特性

- **LRU 缓存**：优先级解析缓存，提升 40x 性能
- **批量处理**：优化的批量验证、解析、评估
- **性能监控**：实时监控操作延迟、吞吐量、缓存命中率
- **上下文压缩**：减少 token 数量，提升上下文利用率

### 质量保证

- **质量评估**：多维度评分（完整性、准确性、一致性、实用性）
- **生命周期管理**：自定义类型的创建、使用、废弃、清理
- **使用监控**：统计 metadata 使用情况，生成改进建议
- **压缩质量**：压缩质量评分，确保关键内容不丢失
