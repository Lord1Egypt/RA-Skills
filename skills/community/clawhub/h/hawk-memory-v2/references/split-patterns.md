# Memory Split Patterns

---

## Two Split Modes

### Mode 1: By Project

```
memory/
├── qujingskills.md     ← qujin-laravel-team Skill
├── feedback.md        ← feedback module
├── context-hawk.md    ← context-hawk Skill
├── laravel.md         ← Laravel framework learning
└── general.md        ← Cross-project content
```

**Best for**: multi-project parallel work

### Mode 2: By Topic

```
memory/
├── team-rules.md         ← Agent collaboration rules
├── user-preferences.md   ← Communication preferences
├── project-status.md     ← Current project progress
├── tech-patterns.md     ← Technical learnings
└── todo.md              ← Cross-project TODOs
```

**Best for**: single project with diverse content types

---

## Split Execution

```bash
hawk split --by-project
hawk split --by-topic
```

Interactive flow:

```
[Context-Hawk] Split mode: by-project

  Scanning memory/ directory...

  Identified:
  ┌──────────────────────────────────────────┐
  │ qujingskills  23 records → qujingskills.md │
  │ feedback       8 records → feedback.md     │
  │ other         5 records → general.md      │
  └──────────────────────────────────────────┘

  [1] Confirm all splits
  [2] Manual adjustment
  [3] Cancel
```

---

## Split Rules

| Content type | → File |
|-------------|--------|
| Skill development/specs | `qujingskills.md` |
| Specific project progress | `project-status.md` |
| User preferences | `user-preferences.md` |
| Team collaboration rules | `team-rules.md` |
| Technical learnings/patterns | `tech-patterns.md` |
| Cross-project TODOs | `todo.md` |

---

## Deduplication on Split

When split finds duplicate records:
1. Keep the newest
2. Mark old record as `[migrated to xxx.md]`
3. Log migration in summary table

---

## After Split — Memory Still Lives in LanceDB

After splitting, all memories still exist in:
1. **Split files** (human-readable)
2. **LanceDB** (vector searchable)

Both stay in sync.

---

## Split ↔ Memory Tier Relationship

| Split file | LanceDB table | Content |
|-----------|---------------|---------|
| qujingskills.md | longterm (scope=qujingskills) | Skill-related |
| user-preferences.md | longterm (category=preference) | User preferences |
| project-status.md | shortterm (category=event) | Progress/milestones |
| tech-patterns.md | longterm (category=pattern) | Technical experience |
| todo.md | working (category=task) | Active tasks |

---

## Split Config File

`.hawk-split-config`:

```json
{
  "mode": "by-project",
  "files": {
    "qujingskills.md": ["skill", "development", "specs", "agent"],
    "feedback.md": ["feedback", "pr", "issue"],
    "laravel.md": ["laravel", "php", "framework"]
  },
  "default_file": "general.md",
  "last_split": "2026-03-29T00:00:00+08:00"
}
```
