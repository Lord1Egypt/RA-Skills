# Usage Guide

## Quick start

```bash
python3 scripts/generate_study_plan.py --seed 20240501 --start-date 2026-10-24
```

Prints a 7-day Markdown table (3 slots per day) to stdout. Each row is
`日期 | 时段 | 学习主题 | 实践内容 | 时长(分钟)`.

## Common variations

```bash
# Plain text
python3 scripts/generate_study_plan.py --seed 42 --format text

# JSON (machine-readable, for piping into other tools)
python3 scripts/generate_study_plan.py --seed 42 --format json

# Three days, two slots per day, 30-minute sessions
python3 scripts/generate_study_plan.py --seed 7 --days 3 --slots-per-day 2 --session-minutes 30

# Override the topic pool with a comma-separated list of names
python3 scripts/generate_study_plan.py --topics "英语,算法,系统设计"

# Use a custom topic-pool JSON file
python3 scripts/generate_study_plan.py --topics ./my-topics.json

# Write the result to a file
python3 scripts/generate_study_plan.py --seed 7 --output plan.md
```

## Reproducibility

- Passing `--seed <int>` makes the output deterministic: the same seed (and the same
  other parameters) always produces the same plan.
- Omitting `--seed` still works; the generator picks a random seed and prints it
  (`> 随机种子（seed）：<n>` in Markdown/text, and a `seed` field in JSON), so the run
  can be reproduced later with `--seed <n>`.

## Constraints baked into the generator

- **Topics**: drawn from a shuffled queue refilled only when empty, so no topic repeats
  until every topic in the pool has been used at least once.
- **Slots**: within a day, start times are distinct and at least 120 minutes apart, and
  the maximum session length is 110 minutes, so no two slots in a day overlap.
- **Duration**: every session is within `[15, 110]` minutes and inside
  `[--session-minutes - 10, --session-minutes + 10]`, rounded to 5 minutes.

## Extending the topic pool

`scripts/topics.json` holds the default pool:

```json
{
  "topics": [
    {"topic": "Python 基础", "practices": ["用列表推导式重写一段循环", "..."]}
  ]
}
```

Add entries to the `topics` array. Each entry needs a `topic` string and a non-empty
`practices` array; if `practices` is omitted, generic practice items are generated from
the topic name. A completely different pool can be supplied with `--topics
/path/to/pool.json`, which uses the same shape (a bare JSON list is also accepted).

## Error handling

The CLI exits with code `2` and prints a Chinese error message to stderr when arguments
are invalid, for example `--days 0`, `--slots-per-day 8`, or an unreadable `--topics`
file.