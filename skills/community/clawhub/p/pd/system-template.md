# Productivity System Template

Use these as the baseline files for `~/productivity/`.

> **废弃路径（不要使用）**：`planning/`、`goals/someday.md`、`goals/`、`projects/`、`tasks/`、`someday/`（v2.3.0 前旧版承诺体系）。
> 复盘文件位置：`reviews/daily/`（日）、`reviews/weekly/`（周）、`reviews/monthly/`（月）。
> 承诺阶梯（v2.3.0）：0_dream（梦想）→ 1_intent（意图）→ 2_queued（项目）→ 3_committed（行动）→ 4_done（完成）→ 5_archived（归档）

---

## inbox/capture.md

```markdown
# Capture

> 快速捕捉，还没来得及整理的东西。每日写，每周清空。

- Raw capture:
- Loose commitment:
- Idea to sort later:
```

## inbox/triage.md

```markdown
# Inbox Triage

> 每个条目问：这个该什么时候做？
> - 今天 → `reviews/daily/YYYY-MM-DD.md`（Today's Focus）
> - 本周 → commitments/3_committed/this-week.md
> - 这周之后 → commitments/0_dream/ideas.md

（当前等待 triage 的条目）
- [ ]
```

## dashboard.md

```markdown
# Productivity Dashboard

## Current Focus
- Top priority:
- Secondary priority:
- Protect this week:

## Active Goals
- Goal:
  - Why it matters:
  - Current milestone:
  - Deadline:

## Active Projects
- Project:
  - Deadline:
  - Next action:
  - Status: 🟢🟡🔴

## Risks
- What is slipping?
- What needs a decision?
```

## commitments/1_intent/active.md

```markdown
# 90-Day Goals（意图阶段）

> 每月底 review 进度。承诺深度：1/6（有意图，待规划为项目）。

## 90-Day Goals

### 1. 学术能力提升
**What**: ___
**Why**: ___
**Progress**: ___%
**Next milestone**: ___
**Deadline**: ___

---

## Monthly Goals

- [ ] ___
```

## commitments/2_queued/active.md

```markdown
# Active Projects（项目阶段）

> 承诺深度：2/6（已规划，待执行）。每个项目完成后归档到 commitments/4_done/ 或 commitments/5_archived/。

## 在进行中

### 项目名称
**状态**: 🟡 进行中
**描述**: ___
**下一步**: ___
**阻塞**: ___
**依赖**: ___
**截止**: ___

---

## 项目收尾标准

每个项目完成后：
1. 这个项目的核心成就是什么？→ 归档到 commitments/4_done/achievements.md
2. 有没有遗留跟进项？→ 归档到 commitments/5_archived/waiting-projects.md
```

## commitments/3_committed/next-actions.md

```markdown
# Next Actions

> 承诺深度：3/6（本周可执行的明确下一步行动）。

- [ ] ___
```

## commitments/3_committed/this-week.md

```markdown
# This Week's Commitments

> 承诺深度：3/6（本周必须/应该完成的事）。

## Must Ship
- [ ] ___

## Important but Flexible
- [ ] ___
```

## commitments/3_committed/waiting.md

```markdown
# Waiting For

> 承诺深度：3/6（等待外部反馈或条件成熟）。定期跟催。

## 等待外部反馈
| 任务 | 等待对象 | 等待内容 | 发起日期 | 状态 |
:|------|---------|---------|---------|------|

## 等待条件成熟
| 任务 | 等待条件 | 触发动作 |
:|------|---------|---------|
```

## commitments/4_done/achievements.md

```markdown
# Done & Achievements

> 承诺深度：4/6（已完成，值得保留经验）。

## YYYY年MM月

### 里程碑
- [x] ___

---

## 经验萃取（用于下一个类似项目）

1. ___
```

## commitments/5_archived/waiting-projects.md

```markdown
# Waiting Projects（归档）

> 承诺深度：5/6（暂停/等待外部的项目）。

## 暂停中
| 项目 | 暂停原因 | 重启条件 |
|------|---------|---------|

## 等待外部反馈
| 项目 | 等待对象 | 等待内容 | 状态 |
```

## commitments/5_archived/waiting-tasks.md

```markdown
# Waiting Tasks（归档）

> 承诺深度：5/6（归档的等待项）。

| 任务 | 等待条件 | 触发动作 |
```

## habits/active.md

```markdown
# Active Habits

## Current Habits

| Habit | Frequency | Trigger | Status | Friction |
|-------|-----------|---------|--------|----------|
| ___ | Daily/Weekly | ___ | 🟢🟡🔴 | ___ |

---

## Habit Design Template（四大定律设计）

**习惯名称**：___
**最终目标行为**：___

**第一定律：让它显而易见**
- 提示公式：我将在 [时间]，于 [地点]，进行 [行为]
- 绑定旧习惯：做完 [___] 后，我立刻做 [新习惯]
- 环境设计：[描述让提示可见的具体布置]

**第二定律：让它有吸引力**
- 喜好绑定：完成习惯后，我能 [___]
- 心态重构："我得去" → "___"

**第三定律：让它简便易行**
- 最小行动（两分钟版本）：___
- 环境简化：减少 [___] 步骤

**第四定律：让它令人愉悦**
- 即时奖励：完成后我会 [打钩/记录/庆祝]
- 追踪方式：[日历打钩/app打卡/纸质记录]

**状态判别**：如果这个最小行动在状态差时仍让我犹豫，需要进一步缩减为：___
```

## reviews/daily/ — 日复盘

> 文件名格式：`YYYY-MM-DD.md`（如 `2026-04-02.md`）
> 模板：自由格式，建议包含 Feel-Good Score + 时间块记录 + Evening Review + Tomorrow's Focus
> 复盘写在**第二天早上**。复盘里写"今日"而非"明日"。

**写入位置**：`~/productivity/reviews/daily/YYYY-MM-DD.md`
**写入时机**：每日结束后，第二天早上完成

## reviews/weekly/ — 周复盘

> 文件名格式：`YYYY-Wnn.md`（如 `2026-W12.md`）
> 模板见：`reviews/weekly/template.md`

**写入位置**：`~/productivity/reviews/weekly/YYYY-Wnn.md`
**写入时机**：每周日

## reviews/monthly/ — 月复盘

> 文件名格式：`YYYY-MM.md`（如 `2026-03.md`）
> 模板见：`reviews/monthly/template.md`

**写入位置**：`~/productivity/reviews/monthly/YYYY-MM.md`
**写入时机**：每月末

## commitments/promises.md

```markdown
# Promises

## 持续承诺
- [x] ___

## 新增承诺
| 承诺 | 对象 | Deadline | 状态 |
:|------|------|---------|------|
```

## commitments/delegated.md

```markdown
# Delegated & External Dependencies

## 已委托
| 委托对象 | 委托内容 | 委托日期 | 状态 | check日期 |
:|---------|---------|---------|------|---------|
| ___ | ___ | ___ | ⏳ | ___ |

## 主动跟进（外部依赖，非委托）
| 事项 | 外部对象 | 等待内容 | 发起日期 | 状态 |
|------|---------|---------|---------|------|
```

## focus/sessions.md

```markdown
# Focus Sessions

## Session Log

| 日期 | 开始时间 | 时长 | 任务类型 | 产出 | 质量评分 |
|------|---------|------|---------|------|---------|
| ___ | ___ | ___min | ___ | ___ | ___/10 |

## Pattern Insights

1. ___
```

## focus/distractions.md

```markdown
# Distractions

## Repeating Patterns

| 情境 | 触发 | 应对 |
|------|------|------|
| ___ | ___ | ___ |
```

## routines/morning.md

```markdown
# Morning Routine

## Startup Defaults

1. 第一件事：
2. 能量状态评估（Feel-Good）：
3. SM 优先：Peak 时间第一块给 SM

## What Must Not Happen
- ___
```

## routines/shutdown.md

```markdown
# Shutdown Routine

## End-of-Day Reset

1. 关闭所有打开的任务（写进 inbox 或归档）
2. 确认明天最重要的事（Tomorrow's Focus）
3. 日志写入 `reviews/daily/YYYY-MM-DD.md`

## Carry-over Rules
- 没完成的 → 写进 inbox，明天再决定优先级
- 有灵感/想法 → 写进 inbox/capture.md
```

## commitments/0_dream/ideas.md

```markdown
# Someday / Maybe（梦想阶段）

> 不承诺，但想探索的方向。每月底 review。
> Someday Audit（每半年一次）：时机成熟了 → 移到 commitments/1_intent/active.md；不感兴趣了 → 删除

## 学术相关
- [ ] ___

## 技能相关
- [ ] ___

## 生活相关
- [ ] ___

## 探索类
- [ ] ___
```
