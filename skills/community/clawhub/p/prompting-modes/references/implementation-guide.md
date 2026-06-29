# OpenClaw 实现指南

## 架构适配

OpenClaw 是一个 LLM Agent 架构，与传统 Python 调用 LLM 的方式不同：
- **传统**: Python 代码调用 LLM API，控制推理流程
- **OpenClaw**: LLM 本身就是 Agent，通过 SKILL.md 指导行为

因此，prompting-modes 技能不需要 Python 代码，而是通过 SKILL.md 中的格式模板和行为规则来引导 LLM 采用不同的推理策略。

---

## 各模式在 OpenClaw 中的实现

### Chain-of-Thought
**实现方式**: 直接按格式模板输出推理过程
**无需特殊工具**: LLM 天然支持逐步推理

```markdown
## 分步推理
**步骤1**: ...
→ 得到: ...
```

### Self-Consistency
**实现方式**: 在同一次回复中生成多条推理路径
**注意**: 不是真正调用 LLM 多次，而是模拟多次采样的效果

```markdown
## 多次采样
**路径1**: ... → 答案A
**路径2**: ... → 答案B
**路径3**: ... → 答案A
```

**局限性**: 真正的 SC 需要多次独立 API 调用，OpenClaw 中是单次回复内模拟。

### Tree-of-Thought
**实现方式**: 生成多个分支 → 自评 → 深入展开
**已内联到 daily-agent**: 作为"模式D：多路径探索"

```markdown
## 生成初始分支
**分支A**: ...
**分支B**: ...
**分支C**: ...

## 评价后深入
淘汰B，深入A和C...
```

### ReAct
**实现方式**: 使用 OpenClaw 的工具调用机制
**天然支持**: Thought → Action → Observation 循环

```
Thought: 需要搜索最新信息
Action: web_search("关键词")
Observation: [搜索结果]
Thought: 基于结果...
```

**工具映射**:
| ReAct Action | OpenClaw 工具 |
|-------------|--------------|
| search | web_search |
| calculate | exec (Python) |
| read_file | read |
| query_db | exec (SQL) |
| browse | browser |

### Plan-and-Execute
**实现方式**: 先输出计划表格，再逐步执行
**与 daily-agent 的关系**: daily-agent 的调度流程就是 P&E

```markdown
## 执行计划
| 步骤 | 任务 | 预期输出 |
|------|------|---------|
| 1 | ... | ... |

## 执行记录
### 步骤1: ...
结果: ...
```

---

## 模式选择指南

### 自动选择逻辑
当用户没有显式指定模式时，按以下优先级：

1. **需要工具** → ReAct
2. **客观题/高准确率** → Self-Consistency
3. **多方案对比** → Tree-of-Thought
4. **步骤≥5** → Plan-and-Execute
5. **需要解释** → Chain-of-Thought
6. **其他** → 直接回答

### 显式触发词
| 触发词 | 模式 |
|--------|------|
| "一步一步"/"解释过程" | CoT |
| "确定吗"/"多验证几次" | SC |
| "几种方案"/"ToT"/"头脑风暴" | ToT |
| "搜索"/"查询"/"实时" | ReAct |
| "计划"/"步骤"/"分步执行" | P&E |

---

## 与其他技能的关系

### daily-agent
- daily-agent 是任务调度中枢，决定"做什么、怎么做"
- prompting-modes 是推理策略工具箱，决定"怎么思考"
- ToT 已内联到 daily-agent 作为"模式D"
- P&E 已内联到 daily-agent 的调度流程中

### 独立使用场景
当用户显式要求某种推理模式时，加载 prompting-modes：
- "用 CoT 模式分析这个问题"
- "用 SC 验证一下答案"
- "用 ReAct 搜索最新信息"

---

## 性能考量

| 模式 | Token 消耗 | 响应时间 | 适用场景 |
|------|-----------|---------|---------|
| CoT | 中 | 中 | 需要解释的推理 |
| SC | 高(5x) | 高 | 高准确率需求 |
| ToT | 高 | 高 | 复杂决策 |
| ReAct | 取决于工具调用次数 | 取决于工具 | 需要外部信息 |
| P&E | 中-高 | 中-高 | 多步骤任务 |

**建议**: 默认直接回答，仅在必要时激活推理模式。
