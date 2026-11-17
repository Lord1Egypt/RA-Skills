# Task Package Structure and Initialization

## Contents

- Naming and placement
- Single and parallel layouts
- Initializer usage
- Localization pass
- Source-of-truth ordering

## 1. Naming and placement

- Default directory: `YYYY-MM-DD_<task_slug>`.
- Use the local task creation or start date; do not rename it as modification time changes.
- Use a stable business slug rather than weak names such as `phase1`, `misc`, or `fixes2`.
- Let project rules select the parent directory, such as `dev_docs/implementation`, an experiment log, a run-control directory, or a user-specified path.
- Update an existing canonical task directory in place instead of creating a synonymous package.
- Project-specific naming and documentation rules take precedence.

## 2. Single-Worker layout

```text
<task-directory>/
├── README.md
├── GOAL.md
├── design/
│   ├── 00_discussion-decisions.md
│   ├── 01_<part-a>.md
│   └── 02_<part-b>.md
├── execution/
│   └── worker-main.md
└── review/
    └── reviewer-main.md
```

Responsibilities:

- `README.md`: purpose, boundaries, reading order, derived status, and resume entry.
- `GOAL.md`: objective, non-goals, roles, three-state work items, part gates, and completion conditions.
- `design/00_discussion-decisions.md`: original goals, confirmed decisions, rejected alternatives, open gates, and sources.
- `design/NN_<part>.md`: executable work items, design, impact scope, validation, and part audit.
- `execution/worker-main.md`: append-only factual Worker receipts.
- `review/reviewer-main.md`: inherited Reviewer findings or explicitly labeled self-review receipts, per-item verdicts, and re-review history.

GOAL, execution, and review use human-readable task/role labels and also retain internal task or subagent IDs, `fork_current` / `reuse_fixed` / `fresh` modes, fork sources, and the pre-execution fork point in technical lineage. Root GOAL stores launch recommendations, provenance, confirmation, and actual values. Do not add a duplicate `LAUNCH.md`.

## 3. Parallel layout

```text
<task-directory>/
├── README.md
├── GOAL.md
├── design/
├── goals/
│   ├── worker-a.md
│   └── worker-b.md
├── execution/
│   ├── worker-a.md
│   └── worker-b.md
├── review/
│   ├── reviewer-a.md
│   └── reviewer-b.md
└── coordination/
    ├── README.md
    ├── lanes.md
    └── integration.md
```

The root GOAL is the aggregate entry and has one writer: the Orchestrator. Each Worker maintains its own GOAL and execution record; each Reviewer maintains its own review record.

## 4. Initializer

The script is `scripts/init_task_package.py` in this skill.

Single Worker:

```bash
python scripts/init_task_package.py \
  --parent /path/to/dev_docs/implementation \
  --slug repair-provider-boundary \
  --title "Repair Provider Boundary" \
  --part service="Service and persistence" \
  --part surface="Agent and tool surface"
```

Parallel:

```bash
python scripts/init_task_package.py \
  --parent /path/to/dev_docs/implementation \
  --slug provider-refactor \
  --title "Provider Refactor" \
  --part core="Core contract" \
  --part adapter="Adapter migration" \
  --parallel \
  --worker core-worker="Core Worker" \
  --worker adapter-worker="Adapter Worker" \
  --assign core-worker=T01 \
  --assign adapter-worker=T02
```

Arguments:

- `--parent`: parent directory.
- `--slug`: stable slug used in `<date>_<slug>`.
- `--title`: human-readable task title.
- `--date`: optional frozen `YYYY-MM-DD`; defaults to local date.
- `--part slug=title`: repeatable; defaults to `main=Main task`.
- `--parallel`: create the parallel layout.
- `--worker id=label`: repeatable in parallel mode; at least two.
- `--assign worker-id=T01,T02`: assign every part exactly once.

The script only creates an English semantic scaffold and never replaces discussion recovery, current-state inspection, or user confirmation.

## 5. Mandatory localization pass

Select the document language using the project rule and conversation-language policy in `SKILL.md`. If it is not English, localize all generated human-facing text before the package is considered ready:

- headings, explanations, table labels, placeholders, and examples;
- generated link labels and lane prose;
- default part title when used.

Preserve file names, links, paths, IDs, commands, model names, enum/status values, code, and quoted evidence. After localization, scan for accidental mixed-language scaffolding while respecting project-mandated exceptions.

## 6. Source-of-truth ordering

Resolve conflicts in this order:

1. current code, artifacts, and external-system facts;
2. exact execution and review evidence;
3. GOAL aggregate state;
4. README summary;
5. historical chat or old plans.

Correct the lower-priority summary rather than altering evidence to make documents appear consistent.
