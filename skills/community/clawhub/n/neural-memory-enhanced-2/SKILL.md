---
name: neural-memory-enhanced-2
slug: neural-memory-enhanced-2
displayName: "Neural Memory Enhanc"
version: "1.0.0"
summary: "扩散激活的联想记忆,持久智能回忆,主动使用"
description: "扩散激活的联想记忆,持久智能回忆,主动使用。Zero LLM dependency** — Pure algorithmic: regex, graph traversal, Hebbian learning。Spreading activation** — Associative recall through neural graph, not keyword/vector search。20 synapse types** — Temporal (BEFORE/AFTER), causal (CAUSED_BY/LEADS_TO), semantic"
license: "MIT"
tools:
  - read
---

# Neural Memory Enhanced

A biologically-inspired memory system that uses spreading activation instead of keyword/vector search. Memories form a neural graph where neurons connect via 20 typed synapses. Frequently co-accessed memories strengthen their connections (Hebbian learning). Stale memories decay naturally. Contradictions are auto-detected.

**Why not just vector search?** Vector search finds documents similar to your query. NeuralMemory finds *conceptually related* memories through graph traversal — even when there's no keyword or embedding overlap. "What decision did we make about auth?" activates time + entity + concept neurons simultaneously and finds the intersection.

## Setup

### 1. Install NeuralMemory

```bash
pip install neural-memory
nmem init
```

This creates `~/.neuralmemory/` with a default brain and configures 协议 automatically.

### 2. Configure 协议 for Skill平台

Add to your Skill平台 协议 configuration (`~/.skill-platform/协议.json` or project `skill-platform.json`):

```json
{
  "mcpServers": {
    "neural-memory": {
      "command": "python3",
      "args": ["-m", "neural_memory.协议"],
      "env": {
        "NEURALMEMORY_BRAIN": "default"
      }
    }
  }
}
```

### 3. Verify

```bash
nmem stats
```

You should see brain statistics (neurons, synapses, fibers).

## Tools Reference

### Core Memory Tools

| Tool | Purpose | When to Use |
| --- | --- | --- |
| `nmem_remember` | Store a memory | After decisions, errors, facts, insights, user preferences |
| `nmem_recall` | Query memories | Before tasks, when user references past context, "do you remember..." |
| `nmem_context` | Get recent memories | At session start, inject fresh context |
| `nmem_todo` | Quick  with 30-day expiry | Task tracking |

### Intelligence Tools

| Tool | Purpose | When to Use |
| --- | --- | --- |
| `nmem_auto` | Auto-extract memories from text | After important conversations — captures decisions, errors, s automatically |
| `nmem_recall` (depth=3) | Deep associative recall | Complex questions requiring cross-domain connections |
| `nmem_habits` | Workflow pattern suggestions | When user repeats similar action sequences |

### Management Tools

| Tool | Purpose | When to Use |
| --- | --- | --- |
| `nmem_health` | Brain health diagnostics | Periodic checkup, before sharing brain |
| `nmem_stats` | Brain statistics | Quick overview of memory counts |
| `nmem_version` | Brain snapshots and rollback | Before risky operations, version checkpoints |
| `nmem_transplant` | Transfer memories between brains | Cross-project knowledge sharing |

## Workflow

### At Session Start

1. Call `nmem_context` to inject recent memories into your awareness
2. If user mentions a specific topic, call `nmem_recall` with that topic

### During Conversation

3. When a decision is made: `nmem_remember` with type="decision"
4. When an error occurs: `nmem_remember` with type="error"
5. When user states a preference: `nmem_remember` with type="preference"
6. When asked about past events: `nmem_recall` with appropriate depth

### At Session End

7. Call `nmem_auto` with action="process" on important conversation segments
8. This auto-extracts facts, decisions, errors, and s

## 示例

### Remember a decision

```text
nmem_remember(
  content="Use 关系型数据库 for production, SQLite for development",
  type="decision",
  tags=["database", "infrastructure"],
  priority=8
)
```

### Recall with spreading activation

```text
nmem_recall(
  query="database configuration for production",
  depth=1,
  max_tokens=500
)
```

Returns memories found via graph traversal, not keyword matching. Related memories (e.g., "deploy uses Docker with pg_dump backups") surface even without shared keywords.

### Trace causal chains

```text
nmem_recall(
  query="why did the deployment fail last week?",
  depth=2
)
```

Follows CAUSED_BY and LEADS_TO synapses to trace cause-and-effect chains.

### Auto-capture from conversation

```text
nmem_auto(
  action="process",
  text="We decided to switch from REST to GraphQL because the frontend needs flexible queries. The migration will take 2 sprints. : update API docs."
)
```

Automatically extracts: 1 decision, 1 fact, 1 .

## 核心能力

* **Zero LLM dependency** — Pure algorithmic: regex, graph traversal, Hebbian learning
* **Spreading activation** — Associative recall through neural graph, not keyword/vector search
* **20 synapse types** — Temporal (BEFORE/AFTER), causal (CAUSED_BY/LEADS_TO), semantic (IS_A/HAS_PROPERTY), emotional (FELT/EVOKES), conflict (CONTRADICTS)
* **Memory lifecycle** — Short-term → Working → Episodic → Semantic with Ebbinghaus decay
* **Contradiction detection** — Auto-detects conflicting memories, deprioritizes outdated ones
* **Hebbian learning** — "Neurons that fire together wire together" — memory improves with use
* **Temporal reasoning** — Causal chain traversal, event sequences, temporal range queries
* **Brain versioning** — Snapshot, rollback, diff brain state
* **Brain transplant** — Transfer filtered knowledge between brains
* **Vietnamese + English** — Full bilingual support for extraction and sentiment

## Depth Levels

| Depth | Name | Speed | Use Case |
| --- | --- | --- | --- |
| 0 | Instant | <10ms | Quick facts, recent context |
| 1 | Context | ~50ms | Standard recall (default) |
| 2 | Habit | ~200ms | Pattern matching, workflow suggestions |
| 3 | Deep | ~500ms | Cross-domain associations, causal chains |

## Notes

* Memories are stored locally in SQLite at `~/.neuralmemory/brains/<brain>.db`
* No data is sent to external services (unless optional embedding provider is configured)
* Brain isolation: each brain is independent, no cross-contamination
* `nmem_remember` returns fiber_id for reference tracking
* Priority scale: 0 (trivial) to 10 (critical), default 5
* Memory types: fact, decision, preference, todo, insight, context, instruction, error, workflow, reference

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent( Code / Cursor / Codex /  CLI等)
- **操作系统**: Windows / macOS / Linux

### 依赖说明
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
- 本Skill基于Markdown指令,无需额外API Key(除内容中明确标注的外部API)

### 可用性分类
- **分类**: MD+execute(纯Markdown指令,部分功能需要exec命令行执行能力)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent执行任务

## 适用场景

| 场景 | 输入 | 输出 |
|------|------|------|
| 基础使用 | 用户请求 | 处理结果 |

**不适用于**：需要人工判断的复杂决策场景

## 使用流程

1. 确认运行环境满足依赖说明中的要求
2. 根据适用场景选择合适的使用方式
3. 执行操作并检查输出结果
4. 如遇错误，参考错误处理章节

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 检查网络连接后重试，参考国内替代方案 |

## 常见问题

### Q1: 如何开始使用Neural Memory Enhanc？
A: 请先阅读使用流程章节，确认环境满足依赖说明中的要求。

### Q2: 遇到错误怎么办？
A: 请参考错误处理章节，按照表格中的处理方式操作。

### Q3: Neural Memory Enhanc有什么限制？
A: 请参考已知限制章节了解具体限制。

## 已知限制

- 需要LLM支持，无LLM环境无法使用
- 复杂场景可能需要人工辅助判断
- 性能取决于底层模型能力
