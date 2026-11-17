---
slug: neurocache-pro
name: neurocache-pro
version: "2.0.0"
displayName: 神经缓存增强
summary: 生物启发联想记忆：扩散激活+赫布学习+矛盾检测，找到向量检索找不到的关联。
license: MIT
description: |-
  面向 AI Agent 的生物启发式联想记忆系统，直击"向量检索找不到概念关联、记忆矛盾无法自动处理、图谱膨胀性能下降"三大痛点。基于扩散激活（spreading activation）替代关键词/向量搜索，记忆形成神经图谱，神经元经 20 种类型化突触连接。

  核心能力包括扩散激活联想检索（通过图遍历找到概念相关记忆，即使无关键词/embedding 重叠）、赫布学习（共访问记忆自动强化连接）、20 种突触类型（时间/因果/语义/情感/冲突）、艾宾浩斯衰减生命周期、矛盾自动检测与降权、深度分级检索（0-3 级速度/深度权衡）、大脑版本快照与回滚、大脑移植跨项目知识迁移。

  适用场景：需要因果链推理的复杂查询、跨领域概念关联发现、长期项目知识沉淀、冲突信息自动识别、需要版本化管理的记忆库、跨项目知识复用。

  差异化：相比向量检索只能找相似文档，本系统通过图遍历找到概念关联记忆（即使无关键词重叠）；矛盾检测自动识别冲突信息并降权过时记忆；深度分级让用户控制速度/深度权衡；版本快照支持回滚。纯算法实现零 LLM 依赖，降低成本。

  触发关键词：联想记忆、神经记忆、扩散激活、赫布学习、知识图谱、矛盾检测、nmem、neural memory、associative
tags:
- 智能代理
- 记忆管理
- 神经网络
tools:
- read
- exec
---

# 神经缓存增强（NeuroCache Pro）

**为什么不用向量检索？** 向量检索只能找与查询相似的文档。NeuroCache 通过图遍历找到*概念关联*的记忆——即使无关键词或 embedding 重叠。"我们当时对认证做了什么决定？"会同时激活时间+实体+概念神经元，找到交集。

## 痛点与对策速查

| 用户痛点 | 发生场景 | 本系统对策 |
|:---|:---|:---|
| 找不到概念关联 | 向量检索只看相似度，错过因果/时间关联 | 扩散激活图遍历，跨类型关联 |
| 记忆矛盾未处理 | 新旧信息冲突，不知信哪个 | 自动矛盾检测 + 时间戳降权过时记忆 |
| 图谱膨胀变慢 | 记忆越多，遍历越慢 | 衰减剪枝 + 分区 + 深度分级 |
| 赫布学习过拟合 | 噪声连接被强化 | 衰减平衡 + 激活阈值控制 |
| 无法回滚 | 错误记忆污染整个图谱 | 大脑版本快照 + 一键回滚 |
| 跨项目知识孤立 | 每个项目记忆独立，无法复用 | 大脑移植 + 过滤迁移 |
| 检索深度无法控制 | 简单查询也走全图遍历 | 4 级深度分级（0-3） |
| 因果链无法追溯 | "为什么部署失败"无法追因 | CAUSED_BY/LEADS_TO 突触链遍历 |

## 核心概念

一切记忆都是**神经元**，通过**突触**连接。频繁共访问的记忆强化连接（赫布学习），陈旧记忆自然衰减，矛盾自动检测。

```text
Entity: { id, content, type, tags, priority, created, last_accessed, decay_score }
Synapse: { from_id, type, to_id, strength, created, last_fired }
```

### 20 种突触类型

| 类别 | 突触类型 | 用途 |
|:---|:---|:---|
| 时间 | BEFORE, AFTER | 事件先后顺序 |
| 因果 | CAUSED_BY, LEADS_TO | 原因与结果追踪 |
| 语义 | IS_A, HAS_PROPERTY, PART_OF | 分类与属性 |
| 情感 | FELT, EVOKES | 情感关联 |
| 冲突 | CONTRADICTS | 矛盾检测 |
| 关联 | SIMILAR_TO, RELATED_TO | 一般关联 |
| 层级 | PARENT_OF, CHILD_OF | 层级结构 |
| 引用 | REFERENCES, CITED_BY | 引用关系 |
| 位置 | LOCATED_AT, CO_OCCURRED | 空间/共现 |
| 动作 | PERFORMED_BY, RESULTED_IN | 行为关联 |

## 快速开始

### 第 1 步：安装

```bash
pip install neural-memory
nmem init
```

创建 `~/.neuralmemory/` 默认大脑并自动配置 MCP。

### 第 2 步：配置 MCP

```json
{
  "mcpServers": {
    "neural-memory": {
      "command": "python3",
      "args": ["-m", "neural_memory.mcp"],
      "env": {
        "NEURALMEMORY_BRAIN": "default"
      }
    }
  }
}
```

### 第 3 步：验证

```bash
nmem stats
```

应显示大脑统计（神经元数、突触数、纤维数）。

## 工具参考

### 核心记忆工具

| 工具 | 用途 | 使用时机 |
|:---|:---|:---|
| `nmem_remember` | 存储记忆 | 决策后、错误后、事实、洞察、用户偏好 |
| `nmem_recall` | 查询记忆 | 任务前、用户引用过去、"你记得..." |
| `nmem_context` | 获取近期记忆 | 会话开始，注入新鲜上下文 |
| `nmem_todo` | 快速 TODO（30 天过期） | 任务跟踪 |

### 智能工具

| 工具 | 用途 | 使用时机 |
|:---|:---|
| `nmem_auto` | 从文本自动提取记忆 | 重要对话后——自动捕获决策/错误/TODO |
| `nmem_recall` (depth=3) | 深度联想召回 | 需跨领域连接的复杂问题 |
| `nmem_habits` | 工作流模式建议 | 用户重复类似动作序列时 |

### 管理工具

| 工具 | 用途 | 使用时机 |
|:---|:---|
| `nmem_health` | 大脑健康诊断 | 定期体检，分享大脑前 |
| `nmem_stats` | 大脑统计 | 快速概览记忆数量 |
| `nmem_version` | 快照与回滚 | 风险操作前，版本检查点 |
| `nmem_transplant` | 跨大脑迁移记忆 | 跨项目知识共享 |

## 深度分级（差异化核心）

| 深度 | 名称 | 速度 | 用途 | Token 消耗 |
|:---|:---|:---|:---|:---|
| 0 | 即时 | <10ms | 快速事实、近期上下文 | 极低 |
| 1 | 上下文 | ~50ms | 标准召回（默认） | 低 |
| 2 | 习惯 | ~200ms | 模式匹配、工作流建议 | 中 |
| 3 | 深度 | ~500ms | 跨领域关联、因果链 | 高 |

### 深度选择指南

```text
快速事实查询（"上次开会什么时候"）      → depth=0
标准回忆（"我们怎么解决 X 的"）          → depth=1
模式识别（"我最近重复做什么"）           → depth=2
复杂关联（"为什么部署总失败"）           → depth=3
```

**成本优化**：默认用 depth=1，仅复杂问题升级到 depth=3。避免所有查询都用 depth=3 导致 token 浪费。

## 矛盾检测机制（差异化核心）

当新记忆与已有记忆通过 CONTRADICTS 突触连接时，系统自动处理：

```text
新记忆存入 → 检查语义重叠 → 发现冲突
  → 创建 CONTRADICTS 突触
  → 比较时间戳与优先级
  → 降权过时/低优先级记忆
  → 标记冲突供用户确认
```

| 冲突类型 | 处理策略 |
|:---|:---|
| 新旧事实矛盾 | 降权旧记忆，保留新记忆为主 |
| 同优先级矛盾 | 标记待用户确认，暂不降权 |
| 高低优先级矛盾 | 低优先级降权 |
| 同时间戳矛盾 | 标记待确认，两者暂存 |

### 矛盾处理示例

```text
旧记忆："数据库用 MySQL"（priority=5, 30 天前）
新记忆："数据库改用 PostgreSQL"（priority=8, 今天）

处理：
1. 创建 CONTRADICTS 突触
2. 降权旧记忆（decay_score += 0.3）
3. 新记忆成为主记忆
4. 标记："检测到数据库决策变更，已更新"

召回时：
  nmem_recall("数据库选择")
  → 返回 PostgreSQL（主）
  → 附注："曾考虑 MySQL（已过时）"
```

## 衰减与剪枝优化（差异化核心）

艾宾浩斯衰减默认参数可能不适合所有场景。本系统提供可调衰减：

| 参数 | 默认 | 说明 | 调优建议 |
|:---|:---|:---|:---|
| initial_decay | 0.1 | 初始衰减率 | 记忆更新快则调高 |
| decay_interval_days | 7 | 衰减计算间隔 | 长期项目调大 |
| min_activation | 0.05 | 最低激活阈值 | 低于此值剪枝 |
| prune_threshold | 0.01 | 剪枝阈值 | 低于此值删除 |
| reinforce_factor | 0.2 | 访问时强化系数 | 调高则记忆更持久 |

### 衰减配置

```json
{
  "decay": {
    "initialDecay": 0.1,
    "intervalDays": 7,
    "minActivation": 0.05,
    "pruneThreshold": 0.01,
    "reinforceFactor": 0.2,
    "autoPrune": true,
    "pruneSchedule": "weekly"
  }
}
```

### 图谱膨胀防护

| 记忆规模 | 性能影响 | 建议措施 |
|:---|:---|:---|
| <1000 神经元 | 无影响 | 正常使用 |
| 1000-5000 | depth=3 略慢 | 启用自动剪枝 |
| 5000-10000 | depth=2/3 明显变慢 | 分区 + 定期深度清理 |
| >10000 | 全深度变慢 | 考虑大脑分区或迁移到 SQLite |

## 工作流

### 会话开始时

1. 调用 `nmem_context` 注入近期记忆到感知
2. 若用户提及特定主题，调用 `nmem_recall` 查询

### 对话进行中

| 情境 | 动作 |
|:---|:---|
| 做出决策 | `nmem_remember` type="decision" |
| 发生错误 | `nmem_remember` type="error" |
| 用户表达偏好 | `nmem_remember` type="preference" |
| 询问过去事件 | `nmem_recall` 选择合适深度 |
| 识别工作流模式 | `nmem_habits` |

### 会话结束时

1. 调用 `nmem_auto` action="process" 处理重要对话片段
2. 自动提取事实、决策、错误、TODO

## 真实场景示例

### 场景 1：因果链追溯

```text
用户："上周部署为什么失败？"

nmem_recall(
  query="部署失败原因",
  depth=2
)

→ 图遍历 CAUSED_BY 突触链：
  部署失败 → CAUSED_BY → 数据库连接超时
  数据库连接超时 → CAUSED_BY → 连接池耗尽
  连接池耗尽 → CAUSED_BY → 未设置 max_connections
  未设置 max_connections → LEADS_TO → 需更新配置规范

返回完整因果链，而非单独的相似记忆。
```

### 场景 2：跨领域关联发现

```text
用户："认证和缓存有什么关系？"

nmem_recall(
  query="认证 缓存 关联",
  depth=3
)

→ 扩散激活同时激活：
  - 认证相关神经元（JWT, session, token）
  - 缓存相关神经元（Redis, TTL, invalidation）
  - 交集发现：token 缓存策略

返回："认证 token 用 Redis 缓存，TTL=3600s，
       上次因缓存未失效导致权限问题（3 周前）"
```

### 场景 3：矛盾自动处理

```text
会话 A（1 月）：
  nmem_remember("API 限流 100 req/min", type="fact", priority=5)

会话 B（2 月）：
  nmem_remember("API 限流调整为 500 req/min", type="fact", priority=8)
  → 检测到与 1 月记忆矛盾
  → 创建 CONTRADICTS 突触
  → 降权旧记忆
  → 标记变更

会话 C（3 月）：
  nmem_recall("API 限流多少")
  → 返回 500 req/min（新，主）
  → 附注：曾为 100 req/min（1 月，已过时）
```

### 场景 4：版本快照与回滚

```text
风险操作前：
  nmem_version snapshot --label "重构前基线"

操作后发现问题：
  nmem_version diff --from "重构前基线" --to current
  → 显示新增/修改/删除的神经元

回滚：
  nmem_version rollback --to "重构前基线"
  → 恢复到快照状态
```

## 记忆类型与优先级

| 类型 | 说明 | 默认优先级 |
|:---|:---|:---|
| fact | 事实 | 5 |
| decision | 决策 | 7 |
| preference | 偏好 | 6 |
| todo | 待办（30 天过期） | 4 |
| insight | 洞察 | 7 |
| context | 上下文 | 3 |
| instruction | 指令 | 8 |
| error | 错误 | 6 |
| workflow | 工作流 | 5 |
| reference | 引用 | 4 |

优先级范围：0（琐碎）到 10（关键），默认 5。高优先级记忆衰减更慢。

## 大脑移植（跨项目知识迁移）

```text
nmem_transplant(
  from="project-a",
  to="project-b",
  filter={
    "types": ["decision", "lesson"],
    "min_priority": 6,
    "tags": ["architecture", "database"]
  }
)

→ 从 project-a 过滤高价值决策和教训
→ 迁移到 project-b
→ 保留原突触结构
→ 标记来源（transplanted_from）
```

## 常见问题 FAQ

**Q1：扩散激活比向量检索好在哪？**
A：向量检索找"相似"文档，扩散激活找"关联"记忆。例如"认证决策"能通过图遍历找到"部署配置"（因部署依赖认证），即使两者无关键词/embedding 重叠。

**Q2：衰减会不会丢重要记忆？**
A：不会。高优先级记忆衰减慢，访问时自动强化（赫布学习）。仅长期未访问且低优先级的记忆会被降权/剪枝。建议重要记忆设 priority>=7。

**Q3：图谱太大影响性能怎么办？**
A：启用自动剪枝（weekly），调整 minActivation 阈值。超过 10000 神经元考虑大脑分区（按项目/领域拆分）或迁移到 SQLite 后端。

**Q4：矛盾检测会误报吗？**
A：可能。系统标记"潜在矛盾"供用户确认，不自动删除。同优先级矛盾暂不降权，等用户确认。

**Q5：零 LLM 依赖是真的吗？**
A：核心检索纯算法（regex + 图遍历 + 赫布学习）。仅 `nmem_auto` 自动提取可选调用 LLM，也可用 regex 模式匹配替代。

## 故障排查

| 现象 | 排查步骤 | 解决方案 |
|:---|:---|:---|
| 召回为空 | `nmem stats` 确认非空 | 检查大脑路径；确认已存入记忆 |
| 召回太慢 | 检查神经元规模 | 降低 depth；启用剪枝；考虑分区 |
| 矛盾未检测 | 检查 CONTRADICTS 突触 | 确认记忆 type/tags 正确 |
| 记忆过早衰减 | 检查 priority 设置 | 提高 priority 到 7+；调低 initialDecay |
| 大脑损坏 | `nmem_health` 诊断 | 从版本快照回滚 |
| 移植失败 | 检查过滤条件 | 放宽 filter；确认 from 大脑存在 |
| MCP 连接失败 | 检查 python3 路径 | 确认 `pip install neural-memory` 成功 |

## 依赖说明

### 运行环境
- **Agent 平台**：支持 SKILL.md 的任意 AI Agent（Claude Code / Cursor / Codex / Gemini CLI 等）
- **操作系统**：Windows / macOS / Linux
- **Python**：3.9+（运行 neural-memory 包）
- **SQLite**：内置（大脑存储后端）

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---|:---|:---|:---|
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |
| neural-memory | Python 包 | 必需 | `pip install neural-memory` |
| MCP 协议 | 运行时 | 必需 | Agent 平台内置或 nmem init 配置 |
| SQLite | 数据库 | 必需 | Python 内置 |

### API Key 配置
- **核心功能无需 API Key**（纯算法实现）
- 可选 embedding provider 配置用于增强语义匹配（非必需）

### 可用性分类
- **分类**：MD+EXEC（Markdown 指令 + exec 命令行执行）
- **说明**：基于 Markdown 的 AI Skill 驱动 Agent 执行神经记忆管理。核心检索纯算法零 LLM 依赖；需安装 neural-memory 包并通过 MCP 提供工具。
