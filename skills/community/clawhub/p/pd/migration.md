# Migration Guide - PD System

## v2.4.0 — 承诺阶梯目录包入 commitments/

**变更**：将 `commitments/0_dream/`~`commitments/5_archived/` 六个目录包入父文件夹 `commitments/`。

### Before

```
~/productivity/
├── 0_dream/
├── 1_intent/
├── 2_queued/
├── 3_committed/
├── 4_done/
└── 5_archived/
```

### After

```
~/productivity/
└── commitments/         # 承诺阶梯父文件夹
    ├── 0_dream/
    ├── 1_intent/
    ├── 2_queued/
    ├── 3_committed/
    ├── 4_done/
    ├── 5_archived/
    └── 承诺阶梯_README.md
```

### Safe Migration

```
mkdir commitments/
mv 0_dream 1_intent 2_queued 3_committed 4_done 5_archived commitments/
mv 承诺阶梯_README.md commitments/
```

---

## v2.3.0 — 承诺阶梯重组

**变更**：`goals/`+`projects/`+`tasks/`+`someday/` → 六级承诺深度体系 `commitments/0_dream/`~`commitments/5_archived/`。

### Before

```
~/productivity/
├── goals/
│   └── active.md
├── projects/
│   ├── active.md
│   └── waiting.md
├── tasks/
│   ├── next-actions.md
│   ├── this-week.md
│   ├── waiting.md
│   └── done.md
└── someday/
    └── ideas.md
```

### After

```
~/productivity/
├── commitments/0_dream/                   # 梦想（不承诺）
│   └── ideas.md
├── commitments/1_intent/                  # 意图（90-day goals）
│   └── active.md
├── commitments/2_queued/                  # 项目（已规划）
│   └── active.md
├── commitments/3_committed/               # 行动（本周承诺）
│   ├── next-actions.md
│   ├── this-week.md
│   └── waiting.md
├── commitments/4_done/                    # 完成（经验保留）
│   └── achievements.md
└── commitments/5_archived/                # 归档（暂停/等待）
    ├── waiting-projects.md
    └── waiting-tasks.md
```

### Safe Migration

1. 创建 `commitments/0_dream/`、`commitments/1_intent/`、`commitments/2_queued/`、`commitments/3_committed/`、`commitments/4_done/`、`commitments/5_archived/` 目录

2. 迁移文件：
   - `someday/ideas.md` → `commitments/0_dream/ideas.md`
   - `goals/active.md` → `commitments/1_intent/active.md`
   - `projects/active.md` → `commitments/2_queued/active.md`
   - `tasks/next-actions.md` → `commitments/3_committed/next-actions.md`
   - `tasks/this-week.md` → `commitments/3_committed/this-week.md`
   - `tasks/waiting.md` → `commitments/3_committed/waiting.md`
   - `tasks/done.md` → `commitments/4_done/achievements.md`
   - `projects/waiting.md` → `commitments/5_archived/waiting-projects.md`
   - `tasks/waiting.md` → `commitments/5_archived/waiting-tasks.md`（如已有，合并）

3. 删除旧目录：`goals/`、`projects/`、`tasks/`、`someday/`

4. 更新所有引用旧路径的 skill 文件（SKILL.md、setup.md、system-template.md、inbox/triage.md、inbox/capture.md）

5. 内部文件的自我引用（如 `commitments/0_dream/ideas.md` 里的"Someday Audit"注释）同步更新

---

## v2.2.0 — 复盘目录重组

**变更**：日/周/月复盘统一收进 `reviews/` 目录；删除5个过时 context 文件。

### Before

```
~/productivity/
├── daily/                    ← 日复盘
├── weekly/                   ← 周复盘 + template.md
├── monthly/                  ← 月复盘 + template.md
└── ...
```

### After

```
~/productivity/
├── reviews/                  ← ★ 统一复盘容器
│   ├── daily/                # 日复盘（YYYY-MM-DD.md）
│   ├── weekly/               # 周复盘（YYYY-Wnn.md）+ template.md
│   └── monthly/              # 月复盘（YYYY-MM.md）+ template.md
└── ...
```

### Safe Migration

1. 创建 `reviews/` 目录

2. 将 `daily/` 整体移入 `reviews/daily/`

3. 将 `weekly/` 整体移入 `reviews/weekly/`

4. 将 `monthly/` 整体移入 `reviews/monthly/`

5. 确认文件都在正确位置：
   - `reviews/daily/YYYY-MM-DD.md`
   - `reviews/weekly/YYYY-Wnn.md`
   - `reviews/monthly/YYYY-MM.md`

6. 更新 skill 文件中所有路径引用（SKILL.md、setup.md、system-template.md）

7. 删除旧 context 文件（已由 skill 维护者完成）：`parent.md`、`creative.md`、`burnout.md`、`entrepreneur.md`、`adhd.md`

---

## v2.1.0 — 清理废弃路径

**变更**：删除 `planning/`、`reviews/`（旧）、`goals/someday.md`，统一日/周/月复盘到 `daily/`、`weekly/`、`monthly/`。

### Safe Migration

1. 检查 `~/productivity/` 现有文件，确认 `daily/`、`weekly/`、`monthly/`、`someday/` 是否存在

2. 如有 `goals/someday.md`，合并到 `someday/ideas.md`，然后删除

3. 如有 `reviews/` 或 `planning/` 下的文件，转移模板内容到 `weekly/template.md` 或 `monthly/template.md`，然后删除旧文件

4. 删除空的 `planning/` 和 `reviews/` 目录

5. 确认各日志文件在正确目录

6. 更新 `~/productivity/memory.md` 中的路径引用

---

## v1.0.4 Productivity Operating System Update

This update keeps the same home folder, `~/productivity/`, but changes the recommended structure from a light memory-only setup into a fuller operating system with named folders for inbox, goals, projects, tasks, habits, commitments, focus, routines, and someday items.

### Before

- `~/productivity/memory.md`
- optional loose notes such as `~/productivity/<topic>.md`

### After

- `~/productivity/memory.md`
- `~/productivity/inbox/`
- `~/productivity/dashboard.md`
- `~/productivity/goals/active.md`
- `~/productivity/projects/`
- `~/productivity/tasks/`
- `~/productivity/habits/`
- `~/productivity/daily/`
- `~/productivity/weekly/`
- `~/productivity/monthly/`
- `~/productivity/commitments/`
- `~/productivity/focus/`
- `~/productivity/routines/`
- `~/productivity/someday/`

## Safe Migration (Legacy)

1. Check whether `~/productivity/` already exists.

2. If it exists, keep `memory.md` exactly as it is.

3. Create the new files without deleting the old ones.

4. If the user has older free-form topic files in `~/productivity/`, map them gradually:
   - current priorities -> `dashboard.md`
   - goals -> `goals/active.md`
   - projects -> `projects/active.md`
   - actionable work -> `tasks/next-actions.md`
   - habits and routines -> `habits/active.md`
   - focus notes -> `focus/sessions.md` or `focus/distractions.md`
   - parked ideas -> `someday/ideas.md`

5. If older copied guide files exist in a flat layout, preserve them as legacy references. Do not delete or rename them automatically.

6. Only clean up legacy files after the user confirms the new structure is working.

## Post-Migration Check

- `memory.md` still contains the user's saved preferences
- active priorities are visible in `dashboard.md`
- next actions live in `tasks/next-actions.md`
- daily/weekly/monthly reviews in the correct directories
- someday items in `someday/ideas.md`
- no legacy file was deleted without explicit user approval
- `goals/someday.md`、`planning/`、`reviews/` fully removed
