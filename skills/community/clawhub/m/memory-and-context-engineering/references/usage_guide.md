# 使用指南

本文档提供各模块的详细使用示例。

## 目录

1. [认知模型构建](#step-7-认知模型构建)
2. [因果链提取](#step-8-因果链提取)
3. [知识缺口识别](#step-9-知识缺口识别)
4. [检索决策与评估](#step-10-检索决策与评估)
5. [状态一致性校验](#step-11-状态一致性校验)
6. [状态推理](#step-12-状态推理)
7. [跨会话关联](#step-13-跨会话关联)
8. [遗忘机制](#step-14-遗忘机制)
9. [多源协调](#step-15-多源协调)
10. [上下文懒加载](#step-16-上下文懒加载)
11. [权限边界控制](#step-17-权限边界控制)
12. [可观测性管理](#step-18-可观测性管理)
13. [结果压缩](#step-19-结果压缩)
14. [任务进度追踪](#step-20-任务进度追踪)
15. [记忆冲突检测](#step-21-记忆冲突检测)
16. [链式推理增强](#step-22-链式推理增强)

---

## Step 7: 认知模型构建

> **注意**: `CognitiveModelBuilder` 是内部实现模块，不建议直接使用。如需构建认知上下文，请使用 `ContextOrchestrator`。

```python
# 此示例仅供参考，实际应用建议使用 ContextOrchestrator
from scripts import CognitiveModelBuilder

builder = CognitiveModelBuilder(session_id="session_001")

# 设置任务上下文
builder.set_task_context(
    goal="实现用户登录功能",
    sub_goals=["数据库设计", "前端表单", "后端验证"],
    current_focus="后端验证逻辑",
)

# 添加已知事实和约束
builder.add_fact(content="用户使用Python 3.9", source="memory", confidence=0.9)
builder.add_constraint("must_use", "bcrypt加密")
builder.add_knowledge_gap(description="SSO集成方案", importance="high")

# 构建认知模型
model = builder.build()
print(model.to_context_string())  # 输出模型可理解的上下文
```

---

## Step 8: 因果链提取

提取文本中的因果关系链，帮助理解问题的根本原因和解决方案。

```python
from scripts import CausalChainExtractor

extractor = CausalChainExtractor()
chains = extractor.extract("登录失败是因为数据库连接超时，连接池配置过小")

for chain in chains:
    print(chain.to_summary())
    # 问题: 登录失败
    # 根本原因: 连接池配置过小
    # 解决方案: 增加连接池大小
```

---

## Step 9: 知识缺口识别

识别当前知识中缺少的内容，指导后续学习或检索。

```python
from scripts import KnowledgeGapIdentifier, KnowledgeType

identifier = KnowledgeGapIdentifier()

# 注册已有知识
identifier.register_knowledge(content="用户使用Python 3.9", knowledge_type=KnowledgeType.FACTUAL)

# 定义所需知识
identifier.define_required(description="数据库连接配置", for_task="配置连接", importance=4)

# 分析缺口
result = identifier.analyze()
print(f"知识缺口: {result.total_gaps}, 覆盖率: {result.coverage_ratio:.1%}")
```

---

## Step 10: 检索决策与评估

> **注意**: `RetrievalQualityEvaluator` 是内部实现模块。使用 `RetrievalDecisionEngine` 决定是否需要检索。

```python
from scripts import RetrievalDecisionEngine

# 检索决策
engine = RetrievalDecisionEngine()
decision = engine.decide(query="如何优化Python代码性能")

if decision.need in ["required", "recommended"]:
    print(f"建议检索: {decision.queries}")
```

---

## Step 11-16: 内部实现模块

以下模块是内部实现，通常不需要直接调用：

- **状态一致性校验** (`StateConsistencyValidator`)
- **状态推理** (`StateInferenceEngine`)
- **跨会话关联** (`CrossSessionMemoryLinker`)
- **遗忘机制** (`MemoryForgettingMechanism`)
- **多源协调** (`MultiSourceCoordinator`)
- **上下文懒加载** (`ContextLazyLoader`)

这些模块的功能已集成到 `ContextOrchestrator` 中，建议直接使用 `ContextOrchestrator` 统一管理。

---

## Step 17: 权限边界控制

> **注意**: `PermissionBoundaryController` 是内部实现模块。

权限控制已集成到 `PrivacyManager` 中，建议使用 `PrivacyManager` 处理访问控制。

```python
from scripts import PrivacyManager, ConsentStatus

privacy_manager = PrivacyManager(user_id="user_123")

# 检查访问权限
if privacy_manager.get_consent_status("memory_storage") != ConsentStatus.GRANTED:
    # 请求用户同意
    privacy_manager.request_consent(
        consent_type="memory_storage",
        description="是否允许存储交互记忆以提供个性化服务？"
    )
```

---

## Step 18: 可观测性管理

> **注意**: `ObservabilityManager` 是内部实现模块。

系统内部已集成监控能力，通常不需要直接调用。如需自定义监控，可以参考以下模式：

```python
# 内部实现示例，仅供参考
from scripts import LatencyTracker, TokenCounter

# 使用 TokenCounter 统计 Token 使用
counter = TokenCounter()
counter.count("这是需要统计的内容", model="gpt-4")
print(f"Token数: {counter.get_total()}")
```

---

## Step 19: 结果压缩

压缩长文本内容，提取关键信息和因果结构。

```python
from scripts import ResultCompressor

compressor = ResultCompressor()
result = compressor.compress_tool_result(
    content="很长的日志内容...",
    target_tokens=1000
)

print(f"压缩率: {result.compression_ratio:.2%}")
print(f"因果链: {len(result.causal_chains)} 个")
```

---

## Step 20: 任务进度追踪

追踪任务执行进度和状态。

```python
from scripts import TaskProgressTracker

tracker = TaskProgressTracker(task_id="task_001", task_name="实现登录功能")
tracker.set_goal(
    goal_id="goal_001",
    goal_name="实现登录",
    success_criteria=["用户可以登录"]
)

tracker.track_step(
    step_id="step_001",
    step_name="设计流程",
    step_type="planning"
)
tracker.start_step("step_001")
tracker.complete_step("step_001", result="流程设计完成")

report = tracker.get_progress_report()
print(f"完成率: {report.completion_rate:.1%}")
```

---

## Step 21: 记忆冲突检测

> **注意**: `MemoryConflictDetector` 是内部实现模块，功能已集成到 `ContextOrchestrator` 中。

---

## Step 22: 链式推理增强

增强推理链的反思能力，支持推理过程中的自我反思和修正。

```python
from scripts import ChainReasoningEnhancer

enhancer = ChainReasoningEnhancer(
    state_capture=capture,
    short_term=short_term,
    long_term=long_term
)

result = enhancer.process_reasoning_step(
    step={
        "thought": "分析代码性能...",
        "need_reflect": True,
        "reflect_reason": "发现信息矛盾"
    },
    step_index=12,
)

if result["should_reflect"]:
    reflection_result = enhancer.execute_reflection(
        signal=result["signal"],
        context_snapshot=result["context_snapshot"]
    )
```

---

## 推荐使用模式

对于大多数应用场景，推荐使用以下核心模块：

```python
from scripts import (
    ContextOrchestrator,
    create_context_orchestrator,
    PrivacyManager,
    ConsentStatus,
)

# 1. 隐私配置
privacy_manager = PrivacyManager(user_id="user_123")
if privacy_manager.get_consent_status("memory_storage") != ConsentStatus.GRANTED:
    privacy_manager.request_consent(
        consent_type="memory_storage",
        description="是否允许存储交互记忆？"
    )

# 2. 创建上下文编排器
orchestrator = create_context_orchestrator(
    user_id="user_123",
    session_id="session_456",
    max_context_tokens=32000,
)

# 3. 存储记忆
orchestrator.store_memory(
    content="用户想要实现登录功能",
    bucket_type="user_intent",
    topic_label="用户登录",
)

# 4. 准备上下文
context = orchestrator.prepare_context(
    user_input="帮我分析这段代码的性能问题",
    system_instruction="你是一个代码分析专家",
    retrieval_results=["性能优化最佳实践"],
    tool_results=["代码分析结果..."],
)

# 5. 使用上下文
print(context.prepared_content)

# 6. 结束会话
final_stats = orchestrator.end_session()
print(f"Token使用: {final_stats.total_tokens}")
```

更多详细信息请参阅：
- [module_index.md](module_index.md) - 模块索引
- [api_class_reference.md](api_class_reference.md) - API 类参考
- [architecture_overview.md](architecture_overview.md) - 架构总览
