---
name: workflow-crystallizer
description: "Analyze memory logs to detect recurring patterns and suggest automations — cron jobs, skills, or workflow shortcuts. The agent builds its own shortcuts over time. Use when: pattern analysis, workflow patterns, recurring tasks, what do I keep doing, suggest automations, crystallize workflows, detect habits, optimize my workflows, what should be automated."
---

# Workflow Crystallizer

Mines memory logs (`memory/YYYY-MM-DD.md`) for recurring patterns — repeated requests,
multi-step workflows, time-correlated tasks — and generates actionable suggestions:
cron jobs, skill drafts, workflow shortcuts, or monitoring proposals.

Unlike a one-shot "analyze my logs" prompt, this skill persists state across runs.
It remembers what it suggested, what was accepted/rejected, and only surfaces new
insights backed by real evidence.

All scripts live in `scripts/` relative to this SKILL.md.

---

## Quick Run (Full Pipeline)

```bash
cd /Users/openclaw/.openclaw/workspace/skills/workflow-crystallizer
python3 scripts/analyze_patterns.py --full | python3 scripts/generate_suggestions.py | python3 scripts/report.py --state-file state.json
```

This analyzes all memory files, generates suggestions, and prints a markdown report.

## Incremental Run (Cached — Recommended)

```bash
cd /Users/openclaw/.openclaw/workspace/skills/workflow-crystallizer
python3 scripts/analyze_patterns.py | python3 scripts/generate_suggestions.py | python3 scripts/report.py --state-file state.json
```

Only processes new/modified memory files. Uses cached events from prior runs.

## Managing Suggestions

Check state: `python3 scripts/state.py` — shows cached dates, events, suggestions.

To accept/reject/snooze: edit `state.json` directly. Set `status` to `accepted`,
`rejected` (add `rejection_reason`), or `snoozed`. Or use `state.py` imports.

Reset everything: `python3 scripts/state.py --reset`

---

## Individual Scripts

Each script accepts `--help`. Key options:

- `analyze_patterns.py`: `--memory-dir PATH`, `--state-file PATH`, `--full`, `--min-confidence 0.4`
- `generate_suggestions.py`: `--state-file PATH`, `--cron-path PATH`, `--clusters FILE`
- `report.py`: `--state-file PATH`, `--output PATH`, `--clusters FILE`, `--suggestions FILE`
- `state.py`: (no args = inspect state), `--reset` (clear everything)

---

## What It Detects

| Pattern Type | Evidence Needed | Suggestion Output |
|---|---|---|
| Recurring request | 3+ occurrences, 2+ days | Workflow shortcut or monitor |
| Multi-step workflow | 2+ occurrences with step similarity | Skill draft |
| Time-correlated | 2+ at similar times/days | Cron job definition |
| Already formalized | Contains "cron", "automated", etc. | Skipped (no suggestion) |
| Project (not pattern) | Same entity, different actions | Skipped |

See `references/pattern-types.md` for detailed detection logic and scoring weights.

---

## How It Avoids Being Annoying

- **Max 3 suggestions per run** — quality over quantity
- **Confidence threshold (60%)** — no low-quality guesses
- **Deduplication** — checks existing crons and skills before suggesting
- **Never repeats** — tracks what was already suggested
- **Snooze** — deferred suggestions resurface after 30 days
- **Rejected = dormant** — only resurfaces at 80%+ confidence with new evidence

---

## Scheduling

Run weekly via cron or heartbeat. Cost: ~5-10K tokens incremental, ~30K first run.

```
Name: Weekly Workflow Crystallizer
Schedule: 0 20 * * 0 (Sunday 8 PM ET)
Message: Run the workflow-crystallizer skill and present any new suggestions.
```

## Troubleshooting

- **No patterns:** Need 3+ days of substantive memory files
- **All filtered:** Existing crons/skills already cover detected patterns
- **State corrupt:** `python3 scripts/state.py --reset`
- **Too noisy:** Increase `min_confidence` in `state.json` config
