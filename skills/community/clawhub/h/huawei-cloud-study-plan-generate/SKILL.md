---
name: huawei-cloud-study-plan-generate
description: |
  Randomly generate a structured, configurable study-practice plan (学习实践表).
  Lays the plan out as day x time-slot cells, assigns every cell a study topic and
  a concrete practice item, keeps topics from repeating until the topic pool is
  exhausted, keeps a day's time slots non-overlapping, varies each session length
  inside a reasonable interval, and prints the result as a Markdown table (or plain
  text / JSON). A --seed flag makes any run reproducible. Implemented with the
  Python 3 standard library only; it does not call the Huawei Cloud CLI, any
  Huawei Cloud SDK, or any REST API, and it touches no cloud resource.
  Triggers include: "生成学习实践表", "随机生成学习计划", "学习安排", "帮我排学习计划",
  "生成学习表", "study plan", "random study plan", "study schedule",
  "learning plan", "practice plan".
tags: [devtools, study-plan, generator, python, utility]
---

# Study Plan Generator

## Overview

This skill produces a random, readable **study-practice plan**. By default it covers
**7 days**, each day with **3 time slots** (morning / afternoon / evening), and every
cell carries a **study topic**, a **practice item**, and a **session length**. It
focuses on producing a plan that is random *but reasonable*:

- **Constraint-respecting randomness** — the same topic is not reused until the whole
  topic pool is exhausted; a day's time slots never overlap; session lengths stay inside
  a bounded interval around `--session-minutes`.
- **Configurable** — number of days, slots per day, topic pool, session length, start
  date and output format are all parameters.
- **Reproducible** — passing `--seed` makes a run deterministic; when omitted, a random
  seed is chosen and printed so the run can be reproduced later.
- **Self-contained** — pure Python 3 standard library, no network, no credentials.

## Prerequisites

- **Python 3.8+** available as `python3` (or `python`) on `PATH`.
- No Huawei Cloud credentials, CLI (KooCLI), SDK, or network access are needed; this
  skill is entirely local.
- `scripts/topics.json` must be present (it ships with the skill) unless a custom topic
  pool is supplied with `--topics`.

## Workflow

1. **Load the topic pool** — `load_topics()` reads `scripts/topics.json` and returns a
   list of `{"topic", "practices"}` entries; `--topics` may override it with a
   comma-separated topic list or a custom JSON pool.
2. **Lay out the grid** — `build_plan(seed, days, slots_per_day, ...)` walks each day and
   each selected time slot (kept in chronological order). Topics are drawn from a
   shuffled queue that is refilled only after it is exhausted, so no topic repeats until
   the pool is used up.
3. **Fill each cell** — a practice item is chosen at random from the topic's practices,
   and the session length is drawn from
   `[session_minutes - 10, session_minutes + 10]` (clamped to `[15, 110]`, rounded to 5
   minutes). All random choices come from `random.Random(seed)`.
4. **Render** — `render_markdown()` / `render_text()` / `render_json()` turn the plan into
   readable output (Markdown table by default).
5. **Emit** — the result goes to standard output, or to a file when `--output` is given.

## Core Commands

```bash
# Default: a 7-day plan (3 slots per day), reproducible with the given seed
python3 scripts/generate_study_plan.py --seed 20240501 --start-date 2026-10-24

# Plain text
python3 scripts/generate_study_plan.py --seed 42 --format text

# JSON (machine-readable)
python3 scripts/generate_study_plan.py --seed 42 --format json

# Custom number of days, slots per day, and session length
python3 scripts/generate_study_plan.py --seed 7 --days 3 --slots-per-day 2 --session-minutes 30

# Override the topic pool with a comma-separated list of names
python3 scripts/generate_study_plan.py --seed 7 --topics "英语,算法,系统设计"

# Use a custom topic-pool JSON file and write the result to a file
python3 scripts/generate_study_plan.py --topics /path/to/topics.json --output plan.md

# Run the bundled unit tests
python3 -m unittest discover -s tests -v
```

The command-line entry point is `scripts/generate_study_plan.py`; the built-in
`scripts/topics.json` is what the examples above read by default.

## Parameter Confirmation

| Parameter | Required | Description | Default |
|-----------|----------|-------------|---------|
| `--days` | No | Number of days to generate | `7` |
| `--slots-per-day` | No | Time slots per day (max 7) | `3` |
| `--topics` | No | Topic pool override: comma-separated names, or a JSON file path | built-in `scripts/topics.json` |
| `--session-minutes` | No | Nominal session length in minutes; actual length varies within ±10 | `45` |
| `--start-date` | No | Start date `YYYY-MM-DD` | today |
| `--seed` | No | Integer seed for reproducible output | random (printed) |
| `--format` | No | Output format: `markdown`, `text`, or `json` | `markdown` |
| `--output` | No | Write the plan to a file instead of stdout | stdout |

## Reference Documents

| Document | Description |
|----------|-------------|
| [references/usage-guide.md](references/usage-guide.md) | Command recipes, reproducibility rules, extending the topic pool |
| [references/verification-method.md](references/verification-method.md) | How the skill is verified (offline unit tests + spot checks) |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria and out-of-scope items |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/iam-policies.md](references/iam-policies.md) | Permission notes (none required) |

## Notes

- The generator is read-only with respect to the cloud: it reads only its local topic
  pool and writes only to standard output or a user-chosen `--output` file.
- Output ordering: within a day, slots are shown in chronological order; days are
  labelled by ISO date plus a Chinese weekday.
- Session lengths are always within `[15, 110]` minutes and vary inside
  `[session_minutes - 10, session_minutes + 10]`, so the plan stays "random but
  reasonable" and a day's slots never collide.
- To expand the pool, add `{"topic", "practices"}` entries to `scripts/topics.json`
  (each entry should keep at least one practice item); no code change is required.