# 记忆体文件模板

本文档提供 `/memories` 目录下各类文件的模板格式。

---

## 1. session_notes.md (短期记忆)

```markdown
# Session Notes

**创建时间**: 2026-04-28 21:00:00
**任务ID**: T-001
**状态**: [in_progress] | [completed] | [blocked]

## 当前任务
[任务描述]

## 进度
- [x] 步骤1
- [ ] 步骤2
- [ ] 步骤3

## 关键变量
- 变量名: 值

## 阻塞项
- [无] | [具体阻塞描述]

## 上下文摘要
[一句话总结当前状态]

---
**最后更新**: 2026-04-28 21:30:00
```

---

## 2. user_preferences.md (用户偏好)

```markdown
# User Preferences

**最后更新**: 2026-04-28

## 代码规范
- Code comments: en-US | zh-CN [confidence: high]
- Indentation: spaces | tabs [confidence: high]

## 沟通风格
- Response length: brief | moderate | detailed [confidence: medium]
- Technical depth: beginner | intermediate | advanced [confidence: low]

## 工具偏好
- [工具名]: [偏好设置] [confidence: medium]

## 项目偏好
- [项目名]:
  - [偏好项]: [值] [confidence: high]

---
**备注**: 用户偏好永不自动删除
```

---

## 3. patterns.md (成功模式)

```markdown
# Success Patterns

**最后更新**: 2026-04-28

## Pattern: [模式名称]

**置信度**: [unconfirmed] | [low] | [medium] | [high] | [validated]
**验证次数**: N
**首次记录**: YYYY-MM-DD
**最后验证**: YYYY-MM-DD

### 触发条件
[在什么情况下使用此模式]

### 模式描述
[具体的方法/策略]

### 成功案例
- [案例ID]: [简要描述]

### 效果
[使用此模式后的预期效果]

---

## Pattern: [下一个模式]
...
```

---

## 4. lessons.md (失败教训)

```markdown
# Failure Lessons

**最后更新**: 2026-04-28

## Lesson: [教训名称]

**严重程度**: [low] | [medium] | [high] | [critical]
**发生时间**: YYYY-MM-DD
**相关Pattern**: [模式名或"N/A"]

### 情境描述
[错误发生的完整情境]

### 根因分析
[为什么会失败]

### 教训提取
1. [教训点1]
2. [教训点2]

### 预防措施
- [应采取的预防措施]

### 相关成功模式
[可以替代的正面模式]

---
```

---

## 5. metrics.md (元认知指标)

```markdown
# Metacognitive Metrics

**报告周期**: 2026-04-01 ~ 2026-04-28
**最后更新**: 2026-04-28 21:00:00

## 任务指标

| 指标 | 数值 | 趋势 |
|------|------|------|
| 总任务数 | N | - |
| 成功任务 | N (X%) | ↑/↓/→ |
| 部分成功 | N (X%) | ↑/↓/→ |
| 失败任务 | N (X%) | ↑/↓/→ |
| 平均完成轮次 | X.X | ↑/↓/→ |

## 记忆体指标

| 指标 | 数值 |
|------|------|
| 记忆命中率 | X% |
| 模式应用次数 | N |
| 新模式创建 | N |
| 教训记录 | N |

## 用户反馈指标

| 指标 | 数值 |
|------|------|
| 用户纠正次数 | N |
| 纠正频率 | X次/任务 |
| 偏好更新次数 | N |

## Self-Improvement Directives

### 当前活跃指令
1. **[优先级-High]**: [指令内容]
2. **[优先级-Medium]**: [指令内容]

### 已完成指令
- [指令]: 已于 YYYY-MM-DD 完成

### 待验证指令
- [指令]: 等待验证
```

---

## 6. Episode (原始案例)

路径: `/memories/evolution/cases/YYYY-MM/[id].md`

```markdown
# Episode: [唯一ID]

**时间**: YYYY-MM-DD HH:MM:SS
**类型**: [success] | [failure] | [partial] | [user_feedback]
**关联任务**: [任务ID或"N/A"]

## 情境 (Context)
[当时的具体情境和输入]

## 动作 (Action)
[Agent 采取的具体行动]
```json
{
  "reasoning": "[推理过程]",
  "tool_calls": ["tool1", "tool2"],
  "output": "[关键输出]"
}
```

## 结果 (Outcome)
[执行后的结果]

## 根因分析 (Root Cause)
[如果是失败：为什么失败]
[如果是成功：为什么成功]

## 模式提取 (Pattern)
[提取的通用模式，可引用 patterns.md 中的模式]

## 标签
- [tag1]
- [tag2]

---
**置信度**: [unconfirmed]
**验证状态**: pending
```
