# Learning Signals Reference

## Signal Types

### 🔴 Correction Signals → `corrections.md`
User is correcting you. Log immediately.

| User Says | Example |
|-----------|---------|
| "不对" / "错了" | "不对，应该用 Python 3.11" |
| "实际上..." | "实际上这个 API 已经废弃了" |
| "我更喜欢..." | "我更喜欢用 bullet list 不用 table" |
| "记得我总是..." | "记得我总是用 tab 不是空格" |
| "别再..." | "别再发半成品给我" |
| "为什么你一直..." | "为什么你一直用错格式" |

**Format:**
```markdown
- [HH:MM] 错误 → 正确
  类型: format|technical|communication|project
  确认: pending (1/3)
```

### 🟡 Preference Signals → `memory.md` (tentative)
User is expressing a preference. Log as tentative, confirm after 3x.

| User Says | Example |
|-----------|---------|
| "我喜欢你..." | "我喜欢你用简洁的方式回复" |
| "总是..." | "总是先搜再答" |
| "永远不要..." | "永远不要用 '咱们'" |
| "我的风格是..." | "我的风格是代码优先解释后补" |

### 🟢 Pattern Candidates → track in memory
Not a correction or preference, but a pattern worth noting.

**Promotion rule:** 同一模式出现 3 次/7天 → 问用户确认为规则

### ⚪ Ignore (不记录)
- 一次性指令："帮我查一下天气"
- 上下文特定："把这个文件改名为 xxx"
- 假设性问题："如果我有 100 万怎么花"

## Memory Tier Rules

| Tier | Location | Size | Load | Decay |
|------|----------|------|------|-------|
| HOT | memory.md | ≤100 lines | Always | Never (confirmed rules) |
| WARM | projects/, domains/ | ≤200 lines/file | On context match | 30 days unused → COLD |
| COLD | archive/ | Unlimited | On explicit query | Never auto-delete |

## Promotion/Demotion Timeline
- Pattern used 3x in 7 days → promote to HOT
- Pattern unused 30 days → demote to WARM
- Pattern unused 90 days → archive to COLD
- **Never delete without asking**

## Self-Reflection Template

After completing significant work:

```markdown
## [Date] Reflection
**Context:** [task type]
**What went well:** [positive]
**What could improve:** [negative]
**Lesson:** [actionable takeaway]
```

Triggers:
- Multi-step task completed
- Feedback received (positive or negative)
- Bug/error fixed
- Output quality noticed as improvable
