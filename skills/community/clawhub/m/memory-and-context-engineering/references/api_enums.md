# API 枚举类型参考

本文档汇总所有模块的枚举类型，供开发者查阅。

## 目录

1. [核心类型枚举（type_defs）](#一核心类型枚举type_defs)
2. [认知模型枚举](#二认知模型枚举)
3. [因果链枚举](#三因果链枚举)
4. [知识缺口枚举](#四知识缺口枚举)
5. [检索决策枚举](#五检索决策枚举)
6. [状态一致性枚举](#六状态一致性枚举)
7. [状态推理枚举](#七状态推理枚举)
8. [跨会话关联枚举](#八跨会话关联枚举)
9. [遗忘机制枚举](#九遗忘机制枚举)
10. [权限控制枚举](#十权限控制枚举)
11. [可观测性枚举](#十一可观测性枚举)

---

## 一、核心类型枚举（type_defs）

> **来源**: `scripts/type_defs.py`
> **导入**: `from scripts.type_defs import *`

### MemoryType（记忆类型）

```python
from scripts.type_defs import MemoryType
```

| 值 | 说明 |
|------|------|
| USER_PROFILE | 用户画像 |
| PROCEDURAL | 程序性记忆 |
| NARRATIVE | 叙事记忆 |
| SEMANTIC | 语义记忆 |
| EMOTIONAL | 情感记忆 |

### MemoryCategory（记忆分类）

```python
from scripts.type_defs import MemoryCategory
```

| 值 | 说明 |
|------|------|
| CORE_IDENTITY | 核心身份 |
| CORE_PREFERENCE | 核心偏好 |
| CORE_SKILL | 核心技能 |
| EXTENDED_BEHAVIOR | 扩展行为 |
| EXTENDED_EMOTION | 扩展情感 |
| EXTENDED_KNOWLEDGE | 扩展知识 |
| EXTENDED_NARRATIVE | 扩展叙事 |
| EXTENDED_REFLECTION | 反思记忆 |

### SemanticBucketType（语义分类桶）

```python
from scripts.type_defs import SemanticBucketType
```

| 值 | 说明 |
|------|------|
| TASK_CONTEXT | 任务上下文桶 |
| USER_INTENT | 用户意图桶 |
| KNOWLEDGE_GAP | 知识缺口桶 |
| EMOTIONAL_TRACE | 情感痕迹桶 |
| DECISION_CONTEXT | 决策上下文桶 |

### QualityDimension（质量评估维度）

```python
from scripts.type_defs import QualityDimension
```

| 值 | 说明 |
|------|------|
| RELEVANCE | 相关性 |
| COMPLETENESS | 完整性 |
| COHERENCE | 连贯性 |
| TIMELINESS | 时效性 |
| DIVERSITY | 多样性 |
| ACTIONABILITY | 可操作性 |

### ScenarioType（场景类型）

```python
from scripts.type_defs import ScenarioType
```

| 值 | 说明 |
|------|------|
| CODING | 编码场景 |
| DEBUGGING | 调试场景 |
| DESIGN | 设计场景 |
| ANALYSIS | 分析场景 |
| LEARNING | 学习场景 |
| PLANNING | 规划场景 |
| REVIEW | 审查场景 |

### PhaseType（阶段类型）

```python
from scripts.type_defs import PhaseType
```

| 值 | 说明 |
|------|------|
| INITIALIZATION | 初始化阶段 |
| PLANNING | 规划阶段 |
| EXECUTION | 执行阶段 |
| REVIEW | 审查阶段 |
| FINALIZATION | 结束阶段 |

### UserStateType（用户状态类型）

```python
from scripts.type_defs import UserStateType
```

| 值 | 说明 |
|------|------|
| ACTIVE | 活跃状态 |
| IDLE | 空闲状态 |
| BUSY | 忙碌状态 |
| OFFLINE | 离线状态 |

### HeatLevel（热度等级）

```python
from scripts.type_defs import HeatLevel
```

| 值 | 说明 |
|------|------|
| HOT | 热门（频繁访问） |
| WARM | 温热（偶尔访问） |
| COLD | 冷门（很少访问） |

### ConflictType（冲突类型）

```python
from scripts.type_defs import ConflictType
```

| 值 | 说明 |
|------|------|
| FACTUAL | 事实冲突 |
| PREFERENCE | 偏好冲突 |
| PRIORITY | 优先级冲突 |
| TEMPORAL | 时间冲突 |

### ResolutionMode（解决模式）

```python
from scripts.type_defs import ResolutionMode
```

| 值 | 说明 |
|------|------|
| AUTOMATIC | 自动解决 |
| MANUAL | 手动解决 |
| HYBRID | 混合解决 |

### TriggerDimension（触发维度）

```python
from scripts.type_defs import TriggerDimension
```

| 值 | 说明 |
|------|------|
| SEMANTIC | 语义触发 |
| TEMPORAL | 时间触发 |
| CONTEXTUAL | 上下文触发 |

### SignalType（信号类型）

```python
from scripts.type_defs import SignalType
```

| 值 | 说明 |
|------|------|
| ACTIVATION | 激活信号 |
| DEACTIVATION | 停用信号 |
| MODIFICATION | 修改信号 |

### InsightType（洞察类型）

```python
from scripts.type_defs import InsightType
```

| 值 | 说明 |
|------|------|
| BEHAVIOR_PATTERN | 行为模式 |
| PREFERENCE_CHANGE | 偏好变化 |
| KNOWLEDGE_GAP | 知识缺口 |
| PERFORMANCE_METRIC | 性能指标 |

### ReflectionTriggerType（反思触发类型）

```python
from scripts.type_defs import ReflectionTriggerType
```

| 值 | 说明 |
|------|------|
| SELF_DETECTED | 模型自检测触发 |
| EXTERNAL_TRIGGER | 外部触发（用户反馈等） |
| SCHEDULED | 定期检查触发 |
| CONTEXT_CHANGE | 上下文变化触发 |

### ReflectionOutcome（反思结果）

```python
from scripts.type_defs import ReflectionOutcome
```

| 值 | 说明 |
|------|------|
| CONFIRMED | 确认正确，无需修改 |
| CORRECTED | 发现问题并已修正 |
| ABORTED | 中止反思 |
| FALSE_POSITIVE | 误报，无需反思 |

### LearningValue（学习价值）

```python
from scripts.type_defs import LearningValue
```

| 值 | 说明 |
|------|------|
| HIGH | 高价值（如修正成功） |
| MEDIUM | 中等价值（如确认正确） |
| LOW | 低价值（如误报） |

### ReflectionSeverity（反思严重程度）

```python
from scripts.type_defs import ReflectionSeverity
```

| 值 | 说明 |
|------|------|
| CRITICAL | 严重 |
| HIGH | 高 |
| MEDIUM | 中 |
| LOW | 低 |

### InsightPriority（洞察优先级）

```python
from scripts.type_defs import InsightPriority
```

| 值 | 说明 |
|------|------|
| CRITICAL | 关键 |
| HIGH | 高 |
| MEDIUM | 中 |
| LOW | 低 |

### SignalStrength（信号强度）

```python
from scripts.type_defs import SignalStrength
```

| 值 | 说明 |
|------|------|
| STRONG | 强 |
| MODERATE | 中等 |
| WEAK | 弱 |

### DecisionType（决策类型）

```python
from scripts.type_defs import DecisionType
```

| 值 | 说明 |
|------|------|
| SINGLE_CHOICE | 单选 |
| MULTI_CHOICE | 多选 |
| YES_NO | 是非 |

### TaskType（任务类型）

```python
from scripts.type_defs import TaskType
```

| 值 | 说明 |
|------|------|
| SIMPLE | 简单任务 |
| COMPLEX | 复杂任务 |
| MULTI_STEP | 多步骤任务 |

### StateEventType（状态事件类型）

```python
from scripts.type_defs import StateEventType
```

| 值 | 说明 |
|------|------|
| PHASE_CHANGE | 阶段变化 |
| TASK_SWITCH | 任务切换 |
| ERROR_OCCURRED | 错误发生 |
| USER_STATE_CHANGE | 用户状态变化 |
| MEMORY_UPDATE | 记忆更新 |

### ConflictSeverity（冲突严重程度）

```python
from scripts.type_defs import ConflictSeverity
```

| 值 | 说明 |
|------|------|
| CRITICAL | 严重：需要立即解决 |
| HIGH | 高：需要尽快解决 |
| MEDIUM | 中：建议解决 |
| LOW | 低：可忽略 |

---

## 二、认知模型枚举

### StepResult（步骤结果）

```python
from scripts.cognitive_model_builder import StepResult
```

| 值 | 说明 |
|------|------|
| SUCCESS | 成功 |
| FAILURE | 失败 |
| IN_PROGRESS | 进行中 |
| SKIPPED | 跳过 |
| BLOCKED | 阻塞 |

### FactSource（事实来源）

```python
from scripts.cognitive_model_builder import FactSource
```

| 值 | 说明 |
|------|------|
| MEMORY | 来自记忆 |
| RETRIEVAL | 来自检索 |
| TOOL | 来自工具返回 |
| USER | 来自用户输入 |
| INFERENCE | 来自推理 |

### ConstraintType（约束类型）

```python
from scripts.cognitive_model_builder import ConstraintType
```

| 值 | 说明 |
|------|------|
| MUST_USE | 必须使用 |
| MUST_AVOID | 禁止使用 |
| PREFERENCE | 用户偏好 |
| RESOURCE | 资源限制 |
| PERMISSION | 权限约束 |

### GapImportance（知识缺口重要程度）

```python
from scripts.cognitive_model_builder import GapImportance
```

| 值 | 说明 |
|------|------|
| CRITICAL | 关键：必须补充 |
| HIGH | 高：强烈建议补充 |
| MEDIUM | 中：建议补充 |
| LOW | 低：可选补充 |

### DecisionStatus（决策状态）

```python
from scripts.cognitive_model_builder import DecisionStatus
```

| 值 | 说明 |
|------|------|
| PENDING | 待决策 |
| MADE | 已决策 |
| REVISED | 已修订 |
| DEFERRED | 已推迟 |

---

## 三、因果链枚举

### CausalRelationType（因果关系类型）

```python
from scripts.causal_chain_extractor import CausalRelationType
```

| 值 | 说明 |
|------|------|
| DIRECT_CAUSE | 直接原因 |
| CONTRIBUTING_FACTOR | 促成因素 |
| ROOT_CAUSE | 根本原因 |
| ENABLING_CONDITION | 使能条件 |
| TRIGGER | 触发因素 |

### ProblemType（问题类型）

```python
from scripts.causal_chain_extractor import ProblemType
```

| 值 | 说明 |
|------|------|
| ERROR | 错误 |
| FAILURE | 失败 |
| ANOMALY | 异常 |
| BOTTLENECK | 瓶颈 |
| CONFLICT | 冲突 |
| GAP | 缺口 |

### SolutionStatus（解决方案状态）

```python
from scripts.causal_chain_extractor import SolutionStatus
```

| 值 | 说明 |
|------|------|
| PROPOSED | 已提出 |
| VALIDATED | 已验证 |
| IMPLEMENTED | 已实施 |
| FAILED | 失败 |

---

## 四、知识缺口枚举

### KnowledgeType（知识类型）

```python
from scripts.knowledge_gap_identifier import KnowledgeType
```

| 值 | 说明 | 建议填充策略 |
|------|------|--------------|
| FACTUAL | 事实性知识 | RETRIEVAL（检索补充） |
| PROCEDURAL | 过程性知识 | TOOL_QUERY（工具查询） |
| CONCEPTUAL | 概念性知识 | RETRIEVAL（检索补充） |
| CONTEXTUAL | 上下文知识 | INFERENCE（推理推断） |
| PREFERENTIAL | 偏好性知识 | USER_CLARIFICATION（用户澄清） |
| TEMPORAL | 时间性知识 | RETRIEVAL（检索补充） |

### GapCategory（缺口类别）

```python
from scripts.knowledge_gap_identifier import GapCategory
```

| 值 | 说明 |
|------|------|
| MISSING_INFO | 缺失信息 |
| UNCERTAINTY | 不确定性 |
| AMBIGUITY | 歧义 |
| CONFLICT | 冲突 |
| OUTDATED | 过时 |
| UNVERIFIED | 未验证 |

### FillStrategy（填充策略）

```python
from scripts.knowledge_gap_identifier import FillStrategy
```

| 值 | 说明 |
|------|------|
| RETRIEVAL | 检索补充 |
| USER_CLARIFICATION | 用户澄清 |
| TOOL_QUERY | 工具查询 |
| INFERENCE | 推理推断 |
| ASSUMPTION | 假设暂时 |

### BlockingLevel（阻塞级别）

```python
from scripts.knowledge_gap_identifier import BlockingLevel
```

| 值 | 说明 |
|------|------|
| CRITICAL | 必须立即解决 |
| HIGH | 强烈建议解决 |
| MEDIUM | 建议解决 |
| LOW | 可选解决 |
| NON_BLOCKING | 不阻塞 |

---

## 五、检索决策枚举

### RetrievalNeed（检索需求级别）

```python
from scripts.retrieval_decision_engine import RetrievalNeed
```

| 值 | 触发条件 |
|------|----------|
| REQUIRED | 知识覆盖率低、不确定性高、故障排查 |
| RECOMMENDED | 复杂查询、知识边界外 |
| OPTIONAL | 探索性查询、已有知识可能足够 |
| UNNECESSARY | 简单查询、已有知识足够 |
| CACHED | 缓存命中 |

### QueryType（查询类型）

```python
from scripts.retrieval_decision_engine import QueryType
```

| 值 | 说明 | 推荐策略 |
|------|------|----------|
| FACTUAL | 事实查询 | HYBRID |
| PROCEDURAL | 过程查询 | KEYWORD_ONLY |
| CONCEPTUAL | 概念查询 | VECTOR_ONLY |
| TROUBLESHOOTING | 故障排查 | HYBRID |
| EXPLORATORY | 探索性查询 | MULTI_PATH |

### RetrievalStrategy（检索策略）

```python
from scripts.retrieval_decision_engine import RetrievalStrategy
```

| 值 | 说明 |
|------|------|
| VECTOR_ONLY | 仅向量检索 |
| KEYWORD_ONLY | 仅关键词检索 |
| HYBRID | 混合检索 |
| SEMANTIC_BUCKET | 语义桶检索 |
| MULTI_PATH | 多路召回 |

### CacheDecision（缓存决策）

```python
from scripts.retrieval_decision_engine import CacheDecision
```

| 值 | 说明 |
|------|------|
| USE_CACHE | 使用缓存 |
| PARTIAL_CACHE | 部分使用缓存 |
| FRESH_RETRIEVAL | 全新检索 |

---

## 六、检索质量枚举

### QualityDimension（质量维度）

```python
from scripts.retrieval_quality_evaluator import QualityDimension
```

| 值 | 权重 | 说明 |
|------|------|------|
| RELEVANCE | 30% | 相关性 |
| COMPLETENESS | 20% | 完整性 |
| FRESHNESS | 15% | 新鲜度 |
| DIVERSITY | 15% | 多样性 |
| COHERENCE | 10% | 连贯性 |
| CREDIBILITY | 10% | 可信度 |

### QualityLevel（质量级别）

```python
from scripts.retrieval_quality_evaluator import QualityLevel
```

| 值 | 评分范围 |
|------|----------|
| EXCELLENT | >= 0.85 |
| GOOD | >= 0.70 |
| ACCEPTABLE | >= 0.50 |
| POOR | >= 0.30 |
| UNACCEPTABLE | < 0.30 |

### ReretrievalNeed（二次检索需求）

```python
from scripts.retrieval_quality_evaluator import ReretrievalNeed
```

| 值 | 说明 |
|------|------|
| NOT_NEEDED | 不需要 |
| RECOMMENDED | 建议 |
| REQUIRED | 需要 |
| URGENT | 紧急 |

---

## 七、状态一致性枚举

### ConsistencyLevel（一致性级别）

```python
from scripts.state_consistency_validator import ConsistencyLevel
```

| 值 | 说明 |
|------|------|
| FULLY_CONSISTENT | 完全一致 |
| MOSTLY_CONSISTENT | 基本一致 |
| PARTIALLY_CONSISTENT | 部分一致 |
| INCONSISTENT | 不一致 |
| SEVERELY_INCONSISTENT | 严重不一致 |

### ConflictSeverity（冲突严重程度）

```python
from scripts.type_defs import ConflictSeverity
```

| 值 | 说明 |
|------|------|
| CRITICAL | 严重：需要立即解决 |
| HIGH | 高：需要尽快解决 |
| MEDIUM | 中：建议解决 |
| LOW | 低：可忽略 |

### ResolutionStrategy（解决策略）

```python
from scripts.state_consistency_validator import ResolutionStrategy
```

| 值 | 说明 |
|------|------|
| AUTO_FIX | 自动修复 |
| LATEST_WINS | 最新优先 |
| PRIORITY_WINS | 优先级优先 |
| USER_DECISION | 用户决策 |
| MANUAL_FIX | 手动修复 |

### StateModule（状态模块）

```python
from scripts.state_consistency_validator import StateModule
```

| 值 | 说明 |
|------|------|
| TASK_PROGRESS | 任务进度状态 |
| SHORT_TERM_MEMORY | 短期记忆状态 |
| LONG_TERM_MEMORY | 长期记忆状态 |
| CONTEXT_ORCHESTRATOR | 上下文编排器状态 |
| GLOBAL_STATE | 全局状态 |

---

## 八、状态推理枚举

### InferenceType（推理类型）

```python
from scripts.state_inference_engine import InferenceType
```

| 值 | 说明 |
|------|------|
| DEDUCTIVE | 演绎推理（从一般到特殊） |
| INDUCTIVE | 归纳推理（从特殊到一般） |
| ABDUCTIVE | 溯因推理（最佳解释） |
| ANALOGICAL | 类比推理（相似情况） |

### InferenceConfidence（推理置信度）

```python
from scripts.state_inference_engine import InferenceConfidence
```

| 值 | 置信度范围 |
|------|------------|
| CERTAIN | >= 0.9 |
| HIGH | >= 0.7 |
| MEDIUM | >= 0.5 |
| LOW | >= 0.3 |
| UNCERTAIN | < 0.3 |

### InferenceSource（推理来源）

```python
from scripts.state_inference_engine import InferenceSource
```

| 值 | 说明 |
|------|------|
| PATTERN | 模式匹配 |
| RULE | 规则推导 |
| HEURISTIC | 启发式 |
| TEMPORAL | 时序推断 |
| CONTEXTUAL | 上下文推断 |

---

## 九、跨会话关联枚举

### LinkStrength（关联强度）

```python
from scripts.cross_session_memory_linker import LinkStrength
```

| 值 | 说明 |
|------|------|
| STRONG | 强关联：同一任务、直接引用 |
| MEDIUM | 中关联：相同主题、相似上下文 |
| WEAK | 弱关联：共享实体、间接关联 |

### LinkType（关联类型）

```python
from scripts.cross_session_memory_linker import LinkType
```

| 值 | 说明 |
|------|------|
| SAME_TASK | 同一任务 |
| SAME_TOPIC | 同一主题 |
| SAME_ENTITY | 同一实体 |
| CONTINUATION | 延续关系 |
| REFERENCE | 引用关系 |
| CONTRADICTION | 矛盾关系 |
| COMPLEMENT | 互补关系 |

### SessionStatus（会话状态）

```python
from scripts.cross_session_memory_linker import SessionStatus
```

| 值 | 说明 |
|------|------|
| ACTIVE | 活跃 |
| PAUSED | 暂停 |
| COMPLETED | 完成 |
| ARCHIVED | 归档 |

---

## 十、遗忘机制枚举

### MemoryImportance（记忆重要性）

```python
from scripts.memory_forgetting_mechanism import MemoryImportance
```

| 值 | 说明 | 遗忘策略 |
|------|------|----------|
| CRITICAL | 关键：永不遗忘 | 保护 |
| HIGH | 高：长期保留 | 延迟遗忘 |
| MEDIUM | 中：中期保留 | 正常遗忘 |
| LOW | 低：短期保留 | 快速遗忘 |
| TRIVIAL | 琐碎：快速遗忘 | 优先遗忘 |

### ForgettingTrigger（遗忘触发因素）

```python
from scripts.memory_forgetting_mechanism import ForgettingTrigger
```

| 值 | 说明 |
|------|------|
| TIME_DECAY | 时间衰减 |
| LOW_ACCESS | 低访问频率 |
| REDUNDANCY | 冗余 |
| IRRELEVANCE | 不相关 |
| CONFLICT | 冲突 |
| EXPLICIT | 显式标记 |

### ForgettingAction（遗忘动作）

```python
from scripts.memory_forgetting_mechanism import ForgettingAction
```

| 值 | 说明 |
|------|------|
| ARCHIVE | 归档：移至冷存储 |
| DEPRIORITIZE | 降权：降低访问优先级 |
| MERGE | 合并：与相似记忆合并 |
| DELETE | 删除：完全移除 |
| KEEP | 保留：不做处理 |

### MemoryState（记忆状态）

```python
from scripts.memory_forgetting_mechanism import MemoryState
```

| 值 | 说明 |
|------|------|
| ACTIVE | 活跃 |
| DORMANT | 休眠 |
| ARCHIVED | 已归档 |
| DELETED | 已删除 |

---

## 十一、权限控制枚举

### AccessAction（访问动作）

```python
from scripts.permission_boundary_controller import AccessAction
```

| 值 | 说明 |
|------|------|
| READ | 读取 |
| WRITE | 写入 |
| DELETE | 删除 |
| SHARE | 分享 |
| EXPORT | 导出 |

### DataCategory（数据类别）

```python
from scripts.permission_boundary_controller import DataCategory
```

| 值 | 说明 |
|------|------|
| USER_PROFILE | 用户资料 |
| MEMORY_DATA | 记忆数据 |
| PREFERENCE_DATA | 偏好数据 |
| BEHAVIOR_DATA | 行为数据 |
| SENSITIVE_DATA | 敏感数据 |

### PermissionLevel（权限级别）

```python
from scripts.permission_boundary_controller import PermissionLevel
```

| 值 | 说明 |
|------|------|
| PUBLIC | 公开 |
| INTERNAL | 内部 |
| CONFIDENTIAL | 机密 |
| RESTRICTED | 限制 |

---

## 十二、可观测性枚举

### AlertLevel（告警级别）

```python
from scripts.observability_manager import AlertLevel
```

| 值 | 说明 |
|------|------|
| INFO | 信息 |
| WARNING | 警告 |
| ERROR | 错误 |
| CRITICAL | 严重 |

### MetricType（指标类型）

```python
from scripts.observability_manager import MetricType
```

| 值 | 说明 |
|------|------|
| COUNTER | 计数器 |
| GAUGE | 仪表 |
| HISTOGRAM | 直方图 |
| SUMMARY | 摘要 |

---

## 相关文档

- [architecture_overview.md](architecture_overview.md) - 全局架构总览
- [memory_types.md](memory_types.md) - 记忆类型详解
