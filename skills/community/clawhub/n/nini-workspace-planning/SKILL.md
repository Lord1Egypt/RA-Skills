---
name: workspace-planning
metadata: {"openclaw":{"emoji":"📅"}}
description: >-
  Use this skill for project schedule management — tracking modules, milestones,
  and delivery phases stored in YAML. Invoke whenever the user asks about: project
  progress or delivery status, module status (planned/in_progress/done/deferred),
  weekly task breakdown, milestone countdowns, risk analysis, linking OpenSpec
  changes to modules, or syncing schedule data to Yunxiao. Triggers on: "planning",
  "schedule", "progress", "milestone", "what's this week", "what's left",
  "mark as done", "排期", "进度", "本周任务", "里程碑", "模块状态", "还剩多少".
  Do NOT trigger for: calendar reminders, weekly work reports, or Yunxiao tasks
  without schedule context.
---

# Workspace Planning

Workspace-level project schedule management. Operates on `planning/schedules/*.yaml`
files that track modules, milestones, and delivery phases.

Each schedule YAML is organized around **functional modules** (not tasks or tickets),
bridging the gap between Yunxiao work items and OpenSpec code changes.

## Prerequisites

| Dependency | Type | Required | Notes |
|------------|------|----------|-------|
| Schedule YAML | data | Yes | `planning/schedules/<project>.yaml` in workspace root |
| yunxiao skill | skill | For sync only | Must be installed before using `planning sync-yunxiao` |

> Do NOT verify prerequisites on skill load. If a command fails due to a missing
> dependency, guide the user through setup step by step.

## When to Use

- User asks about project progress, timeline, or delivery status
- User wants to check what's planned for a specific week
- User mentions milestones, deadlines, or "how much is left"
- User wants to update a module's status or mark something done
- User wants to connect an OpenSpec change to a schedule module
- User needs to create a new project schedule
- User wants to push schedule data to Yunxiao

## Module Status State Machine

```text
planned --> in_progress --> done (terminal)
   |
   +--> deferred --> planned / in_progress
```

Allowed: `planned -> in_progress`, `in_progress -> done`, `planned -> deferred`,
`deferred -> planned`, `deferred -> in_progress`.

Forbidden: any transition out of `done`.

## Module Types

| Type | Description | Key fields |
|------|-------------|------------|
| `feature` | Has UI frames, frontend/backend coordination | `frames`, `design`, `figma`, `backend`, `frontend`, `priority` |
| `infrastructure` | Backend-only, no UI | `description` |

For the complete YAML schema and field reference, read `references/yaml-schema.md`.

## Script

Deterministic operations are handled by `scripts/planning.py`:

```bash
python3 <skill-dir>/scripts/planning.py review                      # Show progress
python3 <skill-dir>/scripts/planning.py update <id> --status done   # Update status
python3 <skill-dir>/scripts/planning.py link <id> --change <name>   # Link change
python3 <skill-dir>/scripts/planning.py week W3                     # Show week modules
```

All commands output JSON for the LLM to format. Use `--file` to specify a schedule YAML
if multiple exist. Always point `--file` at the **main** schedule file (e.g. `sylsmart.yaml`),
not the month files — the script resolves `module_files` references automatically.

Requires: `pip install pyyaml`

### Split vs Inline Modules

Schedules support two layouts:

- **Inline**: `modules:` list directly in the main YAML (simple projects)
- **Split**: `module_files:` list of relative paths, each containing a `modules:` list (large projects)

When using split layout, all read commands (`review`, `week`) merge modules from all
referenced files. Write commands (`update`, `link`) save back to the correct source file.

## Commands

### `planning init <project-name>`

Bootstrap a new schedule YAML for a project. This is interactive (handled by the LLM, not the script).

**Steps:**

1. Ask the user for basic project info:
   - Project title (display name)
   - Timeline start and end dates
   - Team capacity (optional)
2. Ask about milestones (at least one required) — for each: id, title, date, type, deliverable
3. Ask about phases (optional) — or suggest a default monthly split based on timeline
4. Create `planning/schedules/<project-name>.yaml` with the provided structure and an empty `modules: []`
5. Suggest next step: "Add modules manually or describe your feature list and I'll help structure them"

### `planning review`

Show overall schedule progress grouped by phase.

**Steps:**

1. Run `python3 <skill-dir>/scripts/planning.py review` (use `--file` if needed)
2. Format the JSON output for the user
3. Display by phase:

```text
## sylsmart schedule (current: W3)

### month-1: Framework (2/6 done, 33%)
  V core-extraction         infrastructure  done
  V auth                    feature 14f     done
  * project-list            feature 12f     in_progress
  o project-overview        feature 10f     planned
  o common-dialogs          feature 18f     planned
  o core-regression         infrastructure  planned
```

Legend: V done, * in_progress, o planned, - deferred

1. After the module list, add a brief **Risks & Bottlenecks** section (2-4 bullets):
   - Highlight modules with `design: partial` or `pending`
   - Flag weeks where backend capacity is overloaded (many ready_week targets in same week)
   - Note any milestone within 14 days with low completion rate
   - Call out frontend modules that depend on not-yet-ready backend APIs

**Flags:**

- `--week <W>` — Show modules relevant to that week. A module is "relevant" if ANY of these apply: (1) `weeks` contains that week, (2) `backend.ready_week` equals that week, (3) `frontend.mock_from` equals that week. Split output into Backend and Frontend sections with dependency status.
- `--milestones` — Show milestone progress with countdown warnings (highlight if <= 14 days away)

### `planning update <module-id> --status <status>`

Update a module's status.

**Step 1 — Validate** with the script (does NOT write to files):

```bash
python3 <skill-dir>/scripts/planning.py update <module-id> --status <status>
```

The script validates the state machine transition and returns JSON including `source_file`
(the YAML file containing the module). If invalid, it exits with an error.

**Step 2 — Apply** with the Edit tool: use the `source_file` from the JSON output to
locate the module and change its `status:` field. This preserves YAML comments and formatting.

### `planning link <module-id> --change <change-name>`

Associate an OpenSpec change with a module.

**Step 1 — Validate** with the script (does NOT write to files):

```bash
python3 <skill-dir>/scripts/planning.py link <module-id> --change <change-name>
```

The script verifies the change exists and returns JSON with the updated `changes` list,
`source_file`, and whether an auto-transition from `planned` to `in_progress` should apply.

**Step 2 — Apply** with the Edit tool: add the change name to the module's `changes:` list
(or create the field). If `auto_transition` is true, also update `status: in_progress`.

### `planning sync-yunxiao`

Push unlinked modules to Yunxiao as work items.

**Prerequisite:** yunxiao skill must be installed and configured.

**Steps:**

1. Read YAML, find modules where `yunxiao_id` is null or missing
2. List modules to be created, wait for user confirmation
3. Use yunxiao skill to create a work item for each module
4. Write returned work item IDs back to `yunxiao_id` field in YAML
5. Report results; modules with existing `yunxiao_id` are skipped

## Common Mistakes

| Error | Cause | Fix |
|-------|-------|-----|
| Module not found | Typo in module id | Run `planning review` to see all ids |
| Invalid status transition | State machine violation | Check allowed transitions above |
| Change not found | Name mismatch | Verify change exists in `openspec/changes/` |
| No schedule files | Missing YAML | Run `planning init` to create one |
| Yunxiao sync fails | yunxiao skill not installed | Install yunxiao skill first |
