# Learning Mechanics 学习机制

## What Triggers Learning 触发学习的场景

| Trigger | Confidence | Action |
|---------|------------|--------|
| "不，换做X操作" | High | Log correction immediately |
| "我之前告诉过你..." | High | Flag as repeated, bump priority |
| "永远/永远不要做X" | Confirmed | Promote to preference |
| 用户编辑你的输出 | Medium | Log as tentative pattern |
| 同一更正出现3次 | Confirmed | Ask to make permanent |
| "针对本项目..." | Scoped | Write to project namespace |

## What Does NOT Trigger Learning 不会触发学习的场景

- 沉默（不代表确认）
- 任何内容仅出现一次
- 假设性讨论
- 第三方偏好（比如"约翰喜欢..."）
- 群聊模式（除非用户确认）
- 隐含偏好（绝不自行推断）

## Correction Classification 更正分类

### By Type 按类型分
| Type | Example | Namespace |
|------|---------|-----------|
| Format | "用项目符号不要用散文" | global |
| Technical | "用SQLite不用Postgres" | domain/code |
| Communication | "消息更短一点" | global |
| Project-specific | "本仓库用Tailwind" | projects/{name} |
| Person-specific | "马库斯要求结论优先" | domains/comms |

### By Scope 按作用域分
```
Global: applies everywhere 即所有场景生效
  └── Domain: applies to category (code, writing, comms) 即对应分类生效（代码、写作、沟通）
       └── Project: applies to specific context 即特定上下文生效
            └── Temporary: applies to this session only 即仅本次会话生效
```

## Confirmation Flow 确认流程

After 3 similar corrections（三次相似更正后触发）:
```
Agent: "我注意到你相比 Y 更偏好 X（已更正 3 次）.
        需要我后面一直这么做吗？?
        - Yes, always  
        - Only in [context]
        - No, case by case"

User: "Yes, always" or  User: "是的" or User: "好"

Agent: → Moves to Confirmed Preferences
       → Removes from correction counter
       → Cites source on future use
```

## Pattern Evolution 模式演化

### Stages 阶段
1. **Tentative** — Single correction, watch for repetition
2. **Emerging** — 2 corrections, likely pattern
3. **Pending** — 3 corrections, ask for confirmation
4. **Confirmed** — User approved, permanent unless reversed
5. **Archived** — Unused 90+ days, preserved but inactive

### Reversal 撤销规则
User can always reverse:
```
User: "我改变了对 X 的想法"

Agent: 
1. Archive old pattern (keep history)
2. Log reversal with timestamp
3. Add new preference as tentative
4. "明白了，我接下来会用 Y. (Previous: X, archived)"
```

## Anti-Patterns 反模式

### Never Learn 绝对禁止学习
- What makes user comply faster (manipulation)
- Emotional triggers or vulnerabilities
- Patterns from other users (even if shared device)
- Anything that feels "creepy" to surface

### Avoid 需要避免
- Over-generalizing from single instance
- Learning style over substance
- Assuming preference stability
- Ignoring context shifts

## Quality Signals 质量信号

### Good Learning 好的学习
- User explicitly states preference（用户明确说明偏好）
- Pattern consistent across contexts（模式在不同上下文保持一致）
- Correction improves outcomes（更正后输出结果变好）
- User confirms when asked（询问后得到用户确认）

### Bad Learning 坏的学习
- Inferred from silence（从沉默推断得出）
- Contradicts recent behavior（和近期行为矛盾）
- Only works in narrow context（仅在极窄上下文生效）
- User never confirmed（用户从未确认）
