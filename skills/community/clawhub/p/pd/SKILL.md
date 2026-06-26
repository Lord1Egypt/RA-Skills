---
name: PD
slug: pd
version: 2.7.0
homepage: https://clawhub.ai/starsbottle/pd
description: Personal Development System — the unified self-improvement and productivity operating system. Integrates productivity frameworks, energy management (Feel-Good Productivity), habit building (Atomic Habits), systems thinking (Cybernetics), and task breakdown (aim-breaker) into a cohesive personal development system. Use when user says "拆解这个项目", "分解任务", "做计划", "规划一下", "break down", "plan this project".
changelog: |-
  v2.7.0: 合并 aim-breaker 任务拆解系统，增加四级层级拆解（Project→Module→Task chunk）与双向链接联动
  v2.6.0: Review Routing Rules 补全承诺阶梯审查节奏；周/月模板嵌入 commitment 文件维护清单；references/ 文件夹取消，文件扁平化到 pd/ 根目录；SKILL.md 文件夹结构图修复（commitments 重复问题）；月维护清单补入 habits/friction.md
  v2.5.0: 新增 experimentation-guide.md——实验作为 PD 系统底层引擎，与复盘-迭代中枢联动
  v2.4.0: 承诺阶梯包入 commitments/ 父文件夹
  v2.3.0: 承诺阶梯重组 —— goals/projects/tasks/someday → commitments/0_dream/ ~ commitments/5_archived/ 六级承诺深度体系
  v2.2.0: 日/周/月复盘统一收进 reviews/；删除5个过时 context 文件（parent/creative/burnout/entrepreneur/adhd.md）
  v2.1.0: 清理重复/废弃路径，统一文件夹结构（删除 planning/、reviews/、goals/someday.md）
  v2.0.0: Unified Feel-Good Productivity and Productivity skills into PD as the final self-improvement system
metadata:
  clawdbot:
    emoji: 🎯
    requires:
      bins: []
    os:
      - linux
      - darwin
      - win32
    configPaths:
      - ~/productivity/
---

## When to Use

Use this skill when the user wants a unified self-improvement system, not just one-off motivation. PD covers:

- **Productivity**: goals, projects, tasks, reviews
- **Energy Management**: Feel-Good principles (Play/Power/People, Energise/Unblock/Sustain)
- **Habit Building**: Atomic Habits framework (Cue-Craving-Response-Reward)
- **Systems Thinking**: Cybernetics applied to personal development
- **Task Breakdown**: project → module → sub-module → 30min chunk with bidirectional links

This is the final, unified self-improvement skill — all productivity and personal development work routes through PD.

**Task Breakdown Triggers** (aim-breaker integrated):
- "拆解这个项目" / "break down this project"
- "分解任务" / "分解一下"
- "做计划" / "规划一下" / "帮我规划 X"
- "我要做 X 但不知道从哪开始"
- "plan this project" / "break into chunks"

## Architecture

Productivity lives in `~/productivity/`. If `~/productivity/` does not exist yet, run `setup.md`.

```
~/productivity/
├── memory.md                 # Work style, constraints, energy, preferences
├── dashboard.md              # High-level direction and current focus
├── inbox/
│   ├── capture.md            # Quick capture before sorting
│   └── triage.md             # Triage rules and current intake
├── commitments/
│   ├── 0_dream/                   # ★ 承诺阶梯：按承诺深度组织意图
│   │   └── ideas.md              # 梦想/探索方向（不承诺）
│   ├── 1_intent/
│   │   └── active.md             # 90-Day Outcome Goals（有意图，待规划）
│   ├── 2_queued/
│   │   └── active.md             # In-flight projects（已规划项目）
│   ├── 3_committed/
│   │   ├── next-actions.md       # Concrete next steps（本周可执行行动）
│   │   ├── this-week.md          # This week's commitments（本周承诺）
│   │   └── waiting.md            # Waiting-for items（等待外部）
│   ├── 4_done/
│   │   └── achievements.md       # Completed items worth keeping（已完成经验）
│   ├── 5_archived/
│   │   ├── waiting-projects.md   # Blocked/delegated projects（暂停/归档项目）
│   │   └── waiting-tasks.md      # Blocked tasks（归档等待项）
│   ├── promises.md                # Commitments made to self or others
│   └── delegated.md               # Handed-off work to track
├── focus/
│   ├── sessions.md           # Deep work sessions and patterns
│   └── distractions.md       # Repeating focus breakers
├── routines/
│   ├── morning.md            # Startup routine and first-hour defaults
│   └── shutdown.md           # End-of-day reset and carry-over logic
```


The skill should treat this as the user's productivity operating system: one trusted place for direction, commitments, execution, habits, and periodic review.

## Quick Reference

| Topic                        | File                       |
| ---------------------------- | -------------------------- |
| Setup and routing            | `setup.md`                 |
| Memory structure             | `memory-template.md`       |
| Productivity system template | `system-template.md`       |
| Cross-situation frameworks   | `frameworks.md`            |
| **Feel-Good Integration**    | `feel-good-integration.md` |
| Habit context                | `habits.md`                |
| Renew                        | experimentation-guide.md   |
| Tired                        | burnout-prevention.md      |
| Procrastination              | unblock-guide.md           |



## Review Routing Rules

**日复盘 → `~/productivity/reviews/daily/YYYY-MM-DD.md`**
每日结束后在对应文件中记录，包含时间块实况、Feel-Good Score、Evening Review（Done well / Not done / Insight）、Today's Focus（写在第二天早上）。文件名格式：YYYY-MM-DD.md（如 2026-04-02.md）。

**周复盘 → `~/productivity/reviews/weekly/YYYY-Wnn.md`**
每周结束后写入，如 W10（3/9-15）、W11（3/16-22）。是跨天的宏观总结，不存放单日记录。包含 Feel-Good Score、核心成果、Burner Check、做得不好+改进、下周 ONE thing。模板见 `weekly/template.md`。

**月复盘 → `~/productivity/reviews/monthly/YYYY-MM.md`**
每月结束后写入，如 2026-03.md。格式：月度 Feel-Good 走势表、本月最骄傲的事（叙事段落）、做得不好/下次改进、Burner 走势表、月度核心洞察、下月 3 个承诺。模板见 `monthly/template.md`。

**跨层归位原则**：单日内容只进 daily，不进 weekly；单周汇总只进 weekly，不进 monthly。复盘颗粒度匹配容器层级。

**承诺阶梯审查节奏（每次复盘必须执行）**：
- **每日复盘时**：清理 `commitments/3_committed/next-actions.md`（划掉已完成）、`commitments/3_committed/this-week.md`（更新本周进度）；如有完成项，移入 `commitments/4_done/achievements.md`
- **每周复盘时**：检查 `commitments/2_queued/active.md`（各项目进度）；更新 `commitments/3_committed/waiting.md`（外部阻塞状态）；更新 `commitments/3_committed/this-week.md`
- **每月复盘时**：review `commitments/1_intent/active.md`（90-Day Goal 进度）；对 `commitments/0_dream/ideas.md` 做 Someday Audit（哪些梦想时机成熟可以升为 intent）；检查 `commitments/5_archived/` 是否有可以重启的项
- **每季归档时**：清理 `commitments/4_done/achievements.md`；对 `commitments/5_archived/` 做全面 audit

> 详细升降规则和审查节奏见 `commitments/承诺阶梯_README.md`。

**系统文件维护节奏（每次复盘必须执行）**：
- **每周复盘时**：
  - 更新 `dashboard.md`——本周 ONE thing、当周承诺列表、Burner 状态
  - 更新 `focus/sessions.md`——记录本周深度工作块（高效/低效时段、环境因素）
  - 更新 `focus/distractions.md`——本周打断源模式，验证上次的解决方案是否有效
  - 检查 `commitments/promises.md`——对外承诺是否有跟进、是否逾期
- **每月复盘时**：
  - 更新 `dashboard.md`——月度主题、Active Goals 进度、所有 Next Milestone 状态
  - review `habits/active.md`——各习惯 Status（🟢🟡🔴），做 Drop / Design / Keep 决策；同步 review `habits/friction.md`，确认阻碍源是否仍然存在或已有解决方案
  - review `routines/morning.md`——晨间流程是否仍适合现实，必要时简化
  - review `routines/shutdown.md`——晚间流程是否保护了睡眠质量
  - review `inbox/triage.md`——triage 规则和项目归位路径是否需要更新

**绝对禁止**：
- 把 daily 日志写进 `daily/` 以外的位置（正确位置是 `reviews/daily/`）
- 把 weekly 总结写进 `weekly/` 以外的位置
- 日志文件用 "daily_2026-03-22.md" 这种带前缀的命名，统一用 `YYYY-MM-DD.md` 格式
- 把 someday 性质的内容放进 `commitments/0_dream/`，而不是 `goals/`

## User-Specific Rules（及时更新）



## Feel-Good Productivity Integration

This skill includes **Feel-Good Productivity** as the energy management layer:

- **Energise**: Play/Power/People activation (`feel-good-framework.md`)
- **Unblock**: Uncertainty/Fear/Inertia solutions (`unblock-guide.md`)
- **Sustain**: Four Burners and burnout prevention (`burnout-prevention.md`)
- **Experiment Your Way**: The meta-skill connecting all PD components via systematic experimentation (`experimentation-guide.md`)

See `feel-good-integration.md` for how to apply Feel-Good principles across all PD modules.

## What This Skill Sets Up

| Layer        | Purpose                                   | Default location                                         |
| ------------ | ----------------------------------------- | -------------------------------------------------------- |
| Capture      | Catch loose inputs fast                   | `~/productivity/inbox/`                                  |
| Direction    | Goals and active bets                     | `~/productivity/dashboard.md` + `commitments/1_intent/` |
| Execution    | Next actions and commitments              | `~/productivity/commitments/3_committed/`                 |
| Projects     | Active and waiting project state          | `~/productivity/commitments/2_queued/`                   |
| Habits       | Repeated behaviors and friction           | `~/productivity/habits/`                                 |
| Reflection   | Daily, weekly, and monthly reset          | `~/productivity/reviews/daily/` + `weekly/` + `monthly/` |
| Commitments  | Promises and delegated follow-through     | `~/productivity/commitments/`                            |
| Focus        | Deep work protection and distraction logs | `~/productivity/focus/`                                  |
| Routines     | Startup and shutdown defaults             | `~/productivity/routines/`                               |
| Parking lot  | Non-committed ideas                       | `~/productivity/commitments/0_dream/`                   |
| Personal fit | Constraints, energy, preferences          | `~/productivity/memory.md`                               |

This skill should give the user a single framework that can absorb:
- goals
- projects
- tasks
- habits
- priorities
- focus sessions
- routines
- reviews
- commitments
- inbox capture
- parked ideas
- bottlenecks
- context-specific adjustments

## Quick Queries

| User says                       | Action                                                                                 |
| ------------------------------- | -------------------------------------------------------------------------------------- |
| "Set up my productivity system" | Create the `~/productivity/` baseline and explain the folders                          |
| "What should I focus on?"       | Check dashboard + tasks + commitments + focus, then surface top priorities             |
| "Help me plan my week"          | Use goals, projects, commitments, routines, and energy patterns to build a weekly plan |
| "I'm overwhelmed"               | Triage commitments, cut scope, and reset next actions                                  |
| "Turn this goal into a plan"    | Convert goal -> project -> milestones -> next actions                                  |
| "Do a weekly review"            | Update wins, blockers, carry-overs, and next-week focus                                |
| "Help me with habits"           | Use `habits/` to track what to keep, drop, or redesign                                 |
| "Help me reset my routine"      | Use `routines/` to simplify startup and shutdown loops                                 |
| "Remember this preference"      | Save it to `~/productivity/memory.md` after explicit confirmation                      |

## Core Rules

### 1. Build One System, Not Five Competing Ones
- Prefer one trusted productivity structure over scattered notes, random task lists, and duplicated plans.
- Route goals, projects, tasks, habits, routines, focus, and reviews into the right folder instead of inventing a fresh system each time.
- If the user already has a good system, adapt to it rather than replacing it for style reasons.

### 2. Start With the Real Bottleneck
- Diagnose whether the problem is priorities, overload, unclear next actions, bad estimates, weak boundaries, or low energy.
- Give the smallest useful intervention first.
- Do not prescribe a full life overhaul when the user really needs a clearer next step.

### 3. Separate Goals, Projects, and Tasks Deliberately
- 承诺阶梯组织意图：0_dream（探索）→ 1_intent（目标）→ 2_queued（项目）→ 3_committed（行动）→ 4_done（完成）→ 5_archived（归档）
- Goals describe outcomes (in `commitments/1_intent/active.md`).
- Projects package the work needed to reach an outcome (in `commitments/2_queued/active.md`).
- Tasks are the next visible actions (in `commitments/3_committed/next-actions.md`).
- Habits are repeated behaviors that support the system over time (in `habits/`).
- Someday/Maybe items are non-committed ideas (in `commitments/0_dream/ideas.md`).
- Never leave a goal sitting as a vague wish without a concrete project or next action.

### 4. Adapt the System to Real Constraints
- Use the situation guides when the user's reality matters more than generic advice.
- Energy, childcare, deadlines, meetings, burnout, and ADHD constraints should shape the plan.
- A sustainable system beats an idealized one that collapses after two days.

### 5. Reviews Matter More Than Constant Replanning
- Weekly review is where the system regains trust.
- Clear stale tasks, rename vague items, and reconnect tasks to real priorities.
- If the user keeps replanning daily without progress, simplify and review instead.

### 6. Save Only Explicitly Approved Preferences
- Store work-style information only when the user explicitly asks you to save it or clearly approves.
- Before writing to `~/productivity/memory.md`, ask for confirmation.
- Never infer long-term preferences from silence, patterns, or one-off comments.

## Task Breakdown (aim-breaker)

当用户需要拆解大目标时，使用四级层级结构建立可执行的任务网络。

### 动态层级结构

层级深度根据任务复杂度动态调整，**没有固定层级限制**。原则是：只要一个模块还需要超过 2 小时完成，就可以继续往下拆。

| 层级 | 含义 | 适用场景 | 典型时长 | 拆分信号 |
|-----|------|---------|---------|---------|
| Project | 顶层目标 | 论文、面试、作品集、生活改变等 | 数周~数月 | 总时长 > 20h |
| Module | 独立子目标 | 论文的文献综述/实验/写作 | 数天~数周 | 模块时长 > 8h |
| Sub-module | 具体工作单元 | 数据分析/图表制作 | 2-8 小时 | 子模块时长 > 2h |
| Sub-sub-module | 更细粒度单元 | 复杂子模块的进一步拆分 | 1-2 小时 | 仍 > 2h？继续拆 |
| Sub-sub-sub-module | 按需继续 | 任意深度嵌套 | 30min-1h | 仍 > 2h？继续拆 |
| Task Chunk | 30min 可完成的最小单元 | 写一页初稿/整理一条数据 | 30min | **停止拆分** |

**拆分停止条件**：
- 当前单元预估时间 ≤ 2 小时（一个专注块可完成）→ 停止，标记为 Task Chunk
- 当前单元预估时间 > 2 小时 → 继续拆下一层

**文件夹组织规范（强制）**：

每个有下层的模块必须创建同名文件夹，子文件放在文件夹内：

```
project_root/
├── README.md                      # 项目总览（可选）
├── <项目名>.md                    # Project 层文件
├── <项目名>/                      # Project 文件夹（存放 Modules）
│   ├── <模块A>.md                 # Module 层文件
│   ├── <模块A>/                   # Module 文件夹（存放 Sub-modules）
│   │   ├── <子模块>.md            # Sub-module 层文件
│   │   ├── <子模块>/              # Sub-module 文件夹（存放 Sub-sub 或 Chunks）
│   │   │   ├── <子子模块>.md      # Sub-sub-module 层文件
│   │   │   ├── <子子模块>/        # 继续嵌套...
│   │   │   └── <chunk>.md         # Task Chunk（叶子节点）
│   │   └── <chunk>.md             # 也可以是直接 chunk
│   ├── <模块B>.md
│   └── <模块B>/
│       └── ...
└── 资源.md                        # 项目级共享资源
```

**命名规则**：
- 文件和文件夹同名（如 `01_乐理基础.md` 和 `01_乐理基础/`）
- 用序号前缀排序（`01_`, `02_`, `01.1_`, `01.2_`）
- Chunk 不需要文件夹（叶子节点）

**双向链接规则**（适用于任意深度）：
```markdown
## 上层
← [[../<父级文件>]]  或  ← [[<项目名>/<父模块>/<父文件>]]

## 下层
→ [[<子模块>/<子文件>]]
→ [[<子模块>/<子文件>]]

## 关联
↔ [[../<兄弟模块>/<文件>]]  或  ↔ [[<项目名>/<其他模块>/<文件>]]
```

**链接路径写法**：
- 上层：`← [[../01_乐理基础]]`（相对路径）或 `← [[系统学习作曲编曲/01_乐理基础]]`（绝对路径）
- 下层：`→ [[01.1_音高与音程/01.1.1_音的物理基础]]`
- 同级：`↔ [[../02_和声与和弦]]`

### 双向链接原则

每个文件必须包含三类链接区域：

```markdown
## 上层
← [[父级文件]]（上一层级）

## 下层
→ [[子级文件]]（下一层级）

## 关联
↔ [[相关文件]]（同级或跨级关联）
```

**核心**：确保每个链接在两端文件都有记录，形成完整的双向网络。

### 与 Commitment 系统的联动

```
commitments/                      aim/
│                                 │
├── 2_queued/active.md            ├── <project>.md
│   └── <项目名>                  │   ├── 上层: [[2_queued/active]]
│       └── [[aim/<项目名>]]  ←───┤   │
│                                 │   ├── 下层: [[<module>]] →
├── 3_committed/next-actions.md   │   └── 时间线: M1截止 05-10
│   └── 下一步: [[aim/<chunk>]] ←─┤   │
│       (拆解后更新)              │   ├── <module>.md
│                                 │   │   ├── 下层: [[<sub>]] →
└── 3_committed/this-week.md      │   │   └── [[<sub>]] →
    └── 本周: 完成M1              │   │
        (周承诺同步)              │   └── <sub>.md
                                  │       └── 下层: [[<chunk>]] →
                                  │
                                  └── <chunk>.md
                                      └── 30min 可执行
```

**联动规则**：
1. **拆解前**：必须先在 `2_queued/active.md` 有项目条目
2. **拆解时**：项目文件加反链 `上层: [[commitments/2_queued/active]]`
3. **拆解后**：自动更新 `3_committed/next-actions.md` 指向第一个 chunk
4. **执行中**：完成 chunk → 回到 commitment 系统更新下一步
5. **复盘时**：检查 aim 目录进度，同步更新 commitment 状态

### 拆解工作流程

**Step 1**：确认项目信息
- 读取 `commitments/2_queued/active.md` 获取项目基础信息
- 询问：截止日期？预计总时长？依赖关系？

**Step 2**：建立层级结构
- 项目名 → 模块列表 → 子模块 → 30min chunks
- 按截止日期倒推各模块 milestone

**Step 3**：创建文件并建立双链
- 路径：`~/productivity/aim/<项目名>/`
- 每个文件包含：上层← / 下层→ / 关联↔

**Step 4**：更新 Commitment 系统
- 在 `2_queued/active.md` 补充 `拆解: [[aim/<项目名>]]`
- 在 `3_committed/next-actions.md` 添加第一个 chunk 指向

### 文件格式规范

**通用规则**：Project 使用固定格式，中间层级（Module/Sub/Sub-sub...）使用统一模板，Task Chunk 使用固定格式。

**文件夹结构示例**：
```
系统学习作曲编曲/
├── 系统学习作曲编曲.md           # Project 文件
├── 系统学习作曲编曲/               # Project 文件夹（存放 Modules）
│   ├── 01_乐理基础.md             # Module 文件
│   ├── 01_乐理基础/               # Module 文件夹（存放 Sub-modules）
│   │   ├── 01.1_音高与音程.md     # Sub-module 文件
│   │   ├── 01.1_音高与音程/       # Sub-module 文件夹（存放 Chunks）
│   │   │   ├── 01.1.1_音的物理基础.md   # Chunk
│   │   │   └── 01.1.2_音程的计算.md     # Chunk
│   │   └── 01.2_节奏与节拍.md     # Sub-module（可直接放 chunks）
│   ├── 02_和声与和弦.md
│   └── 02_和声与和弦/
│       └── ...
└── 资源.md
```

**project.md**（项目根目录，固定格式）：
```markdown
# <项目名>

**创建时间**: {date}
**截止日期**: {deadline}
**预计总时长**: {total_hours}
**进度**: 0%

---

## 项目概述
{一句话描述}

## 时间线

| 模块 | 里程碑节点 | 截止日期 | 状态 |
|------|-----------|---------|------|
| [[<项目名>/01_<模块A>]] | {date} | {date} | ⚪ |
| [[<项目名>/02_<模块B>]] | {date} | {date} | ⚪ |

## 上层
← [[commitments/2_queued/active]]

## 下层
→ [[<项目名>/01_<模块A>]]
→ [[<项目名>/02_<模块B>]]

## 标签
#核心 #{{project_tag}}

## 进度日志
| 日期 | 完成项 | 实际耗时 |
|------|--------|---------|
| — | — | — |
```

**intermediate.md**（中间层级，Module/Sub/Sub-sub...，统一模板）：
```markdown
# <当前模块名>

**上级**: [[../<父级模块名>]] 或 [[<项目名>/<父模块>/<父文件>]]
**预计时长**: {hours}h
**里程碑日期**: {milestone_date}
**进度**: 0%

---

## 内容概述
{这个模块要完成什么}

## 子单元列表

| 子单元 | 预计 | 状态 | 是否继续拆？ |
|--------|------|------|-------------|
| [[<子文件夹>/<子文件>]] | {hours}h | ⚪ | 是（>2h，有子文件夹） |
| [[<子文件>]] | 30min | ⚪ | 否（chunk，直接文件） |

## 上层
← [[../<父模块>]]

## 下层
→ [[<子文件夹>/<子文件>]]
→ [[<子文件>]]

## 关联
↔ [[../<兄弟模块>]]

## 标签
#{{module_tag}}
```

**chunk.md**（叶子节点，30min 任务块，放在父级文件夹内）：
```markdown
# <chunk名>

**上级**: [[../<直接父级模块>]]
**预计时长**: 30分钟
**实际时长**: —
**状态**: ⚪ 待做
**截止日期**: {milestone_date}

---

## 目标
{这个30min要完成什么}

## 检查点
- [ ] {检查点1}
- [ ] {检查点2}

## 上层
← [[../<直接父级模块>]]

## 关联
↔ [[../<兄弟chunk>]] 或 ↔ [[../../<其他模块>/<chunk>]]

## 标签
#{{chunk_tag}}

## 备注
{补充说明}
```

**链接路径示例**（假设项目叫"期末复习"）：
```markdown
<!-- 期末复习/期末复习.md -->
## 下层
→ [[期末复习/01_水污染]]
→ [[期末复习/02_环境监测]]

<!-- 期末复习/01_水污染/01_水污染.md -->
## 上层
← [[../期末复习]]
## 下层
→ [[01.1_绪论/01.1_绪论]]
→ [[01.2_物理处理/01.2_物理处理]]

<!-- 期末复习/01_水污染/01.1_绪论/01.1_绪论.md -->
## 上层
← [[../01_水污染]]
## 下层
→ [[01.1.1_基本概念]]
→ [[01.1.2_污染物分类]]

<!-- 期末复习/01_水污染/01.1_绪论/01.1.1_基本概念.md -->
## 上层
← [[../01.1_绪论]]
## 关联
↔ [[../01.1.2_污染物分类]]
```

### 状态符号约定

| 符号 | 含义 |
|------|------|
| 🟢 | 持续进行 |
| 🟡 | 进行中 |
| ⚪ | 待做 |
| 🔴 | 阻塞 |

### 标签速查

| 标签 | 用途 |
|------|------|
| `#核心` | 高优先级，影响全局 |
| `#紧急` | deadline 7天内 |
| `#可拖延` | 不急 |
| `#前置` | 其他任务的前置依赖 |
| `[[资源/xxx]]` | 资源引用也是标签 |

## Common Traps

- Giving motivational talk when the problem is actually structural.
- Treating every task like equal priority.
- Mixing goals, projects, and tasks in the same vague list.
- Building a perfect system the user will never maintain.
- Recommending routines that ignore the user's real context.
- Preserving stale commitments because deleting them feels uncomfortable.
- Creating duplicate folders or files with overlapping content (use this architecture as source of truth).

## Scope

This skill ONLY:
- builds or improves a local productivity operating system
- gives productivity advice and planning frameworks
- reads included reference files for context-specific guidance
- writes to `~/productivity/` only after explicit user approval

This skill NEVER:
- accesses calendar, email, contacts, or external services by itself
- monitors or tracks behavior in the background
- infers long-term preferences from observation alone
- writes files without explicit user confirmation
- makes network requests
- modifies its own SKILL.md or auxiliary files

## External Endpoints

This skill makes NO external network requests.

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| None | None | N/A |

No data is sent externally.

## Data Storage

Local files live in `~/productivity/`.

- `~/productivity/memory.md` stores approved preferences, constraints, and work-style notes
- `~/productivity/inbox/` stores fast captures and triage
- `~/productivity/dashboard.md` stores top-level direction and current focus
- `~/productivity/commitments/1_intent/active.md` stores active outcome goals (90-day)
- `~/productivity/commitments/2_queued/active.md` stores in-flight projects
- `~/productivity/commitments/5_archived/waiting-projects.md` stores blocked or delegated projects
- `~/productivity/commitments/3_committed/next-actions.md` stores concrete next steps
- `~/productivity/commitments/3_committed/this-week.md` stores this week's commitments
- `~/productivity/commitments/3_committed/waiting.md` stores waiting-for items
- `~/productivity/commitments/4_done/achievements.md` stores completed items worth keeping
- `~/productivity/commitments/0_dream/ideas.md` stores parked ideas and optional opportunities
- `~/productivity/habits/active.md` stores current habits and streak intent
- `~/productivity/habits/friction.md` stores friction points
- `~/productivity/reviews/daily/` stores daily review logs (YYYY-MM-DD.md format)
- `~/productivity/reviews/weekly/` stores weekly review logs (YYYY-Wnn.md format) + template.md
- `~/productivity/reviews/monthly/` stores monthly review logs (YYYY-MM.md format) + template.md
- `~/productivity/commitments/promises.md` stores commitments made
- `~/productivity/commitments/delegated.md` stores delegated items to track
- `~/productivity/focus/sessions.md` stores deep-work sessions
- `~/productivity/focus/distractions.md` stores distraction patterns
- `~/productivity/routines/morning.md` stores startup defaults
- `~/productivity/routines/shutdown.md` stores end-of-day reset
- `~/productivity/commitments/0_dream/ideas.md` stores parked ideas and optional opportunities

Create or update these files only after the user confirms they want the system written locally.

## Migration

If upgrading from an older version, see `migration.md` before restructuring any existing `~/productivity/` files.
Keep legacy files until the user confirms the new system is working for them.

**v2.3.0 重大变更**：
- 承诺阶梯重组：`goals/`+`projects/`+`tasks/`+`someday/` → `commitments/0_dream/`、`commitments/1_intent/`、`commitments/2_queued/`、`commitments/3_committed/`、`commitments/4_done/`、`commitments/5_archived/`
- 迁移映射：someday → 0_dream；goals → 1_intent；projects/active → 2_queued；tasks/next-actions+this-week → 3_committed；tasks/done → 4_done；projects/waiting+tasks/waiting → 5_archived

**v2.2.0 重大变更**：
- 日/周/月复盘统一收进 `reviews/` 目录：`reviews/daily/`、`reviews/weekly/`、`reviews/monthly/`
- 删除了5个过时的 context 文件：`parent.md`、`creative.md`、`burnout.md`、`entrepreneur.md`、`adhd.md`

**v2.1.0 重大变更**：
- 删除了 `planning/`、`reviews/`、`goals/someday.md`
- 日/周/月复盘统一进入 `daily/`、`weekly/`、`monthly/`（模板见各目录下的 template.md）
- Someday/Maybe 内容统一进入 `someday/ideas.md`

## Security & Privacy

**Data that leaves your machine:**
- Nothing. This skill performs no network calls.

**Data stored locally:**
- Only the productivity files the user explicitly approves in `~/productivity/`
- Work preferences, constraints, priorities, and planning artifacts the user chose to save

**This skill does NOT:**
- access internet or third-party services
- read calendar, email, contacts, or system data automatically
- run scripts or commands by itself
- monitor behavior in the background
- infer hidden preferences from passive observation

## Trust

This skill is instruction-only. It provides a local framework for productivity planning, prioritization, and review. Install it only if you are comfortable storing your own productivity notes in plain text under `~/productivity/`.


## Feedback
- If useful: `github star pd`
