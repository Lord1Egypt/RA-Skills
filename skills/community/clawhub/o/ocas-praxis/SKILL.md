---
name: ocas-praxis
description: Bounded behavioral refinement loop. Records outcomes, extracts micro-lessons from repeated patterns, consolidates them into capped active behavior shifts, applies shifts at runtime, and generates plain-language debriefs. Use when recording outcomes, extracting lessons, managing behavior shifts, generating runtime briefs, or producing debriefs. Do not use for general memory, personality rewriting, or knowledge storage.
metadata: {"openclaw":{"emoji":"🔄"}}
---

# Praxis

Praxis improves future agent behavior through a bounded refinement loop. It records outcomes, extracts lessons from repeated patterns, consolidates them into a small active set of behavior shifts, and produces auditable debriefs.

Praxis is not a diary, general memory system, or self-rewriting identity layer. It is a bounded behavioral refinement loop.

## When to use

- Record a task outcome, failure, success, or correction
- Extract lessons from repeated patterns
- Review or manage active behavior shifts
- Generate the current runtime brief (active shifts only)
- Produce a debrief explaining what changed and why

## When not to use

- General knowledge storage — use Elephas
- Preference tracking — use Taste
- One-off trivia or domain facts
- Broad autobiographical summaries
- Silent personality mutation

## Responsibility boundary

Praxis owns bounded behavioral refinement: events, lessons, shifts, and debriefs.

Praxis does not own: general memory (Elephas), preference persistence (Taste), pattern discovery (Corvus), communications (Dispatch), skill evaluation (Mentor).

Praxis receives BehavioralSignal files from Corvus. Praxis decides whether to act on each signal.

## Commands

- `praxis.event.record` — record a completed event or outcome with evidence
- `praxis.lesson.extract` — derive micro-lessons from recorded events
- `praxis.shift.propose` — propose a new behavior shift from lessons
- `praxis.shift.list` — list all shifts with status
- `praxis.shift.activate` — activate a proposed shift (enforces cap)
- `praxis.shift.expire` — expire or reject a shift with reason
- `praxis.runtime.brief` — generate runtime brief with active shifts only
- `praxis.debrief.generate` — produce a plain-language debrief
- `praxis.status` — event count, active shifts, cap usage, last debrief
- `praxis.journal` — write journal for the current run; called at end of every run

## Core loop

1. Record event → 2. Extract lessons (if pattern detected) → 3. Propose shift → 4. Activate (if cap allows) → 5. Generate debrief

## Hard constraints

- No autonomous identity rewriting
- No silent safety boundary changes
- No unlimited behavior rule accumulation
- Only active shifts influence runtime
- Maximum 12 active shifts (configurable)
- Every shift must trace to recorded events

## Capping and consolidation rules

Default cap: 12 active shifts. When at cap and a new shift is proposed: merge overlapping shifts, replace a weaker shift, or reject the new shift. No duplicate or contradictory active shifts.

## Runtime injection rules

The runtime brief is a compact list of active shifts only. Target: 3-12 items. Imperative, behavior-facing, free of historical clutter. Not a narrative log.

## Inter-skill interfaces

Praxis receives BehavioralSignal files from Corvus at: `~/openclaw/data/ocas-praxis/intake/{signal_id}.json`

Praxis checks its intake directory during `praxis.event.record` and during any scheduled pass. Praxis decides whether to record each signal as an event and extract a lesson. It is not obligated to act on every signal.

After processing each file, move to `intake/processed/`.

See `spec-ocas-interfaces.md` for the BehavioralSignal schema and handoff contract.

## Storage layout

```
~/openclaw/data/ocas-praxis/
  config.json
  events.jsonl
  lessons.jsonl
  shifts.jsonl
  debriefs.jsonl
  decisions.jsonl
  intake/
    {signal_id}.json
    processed/
  reports/

~/openclaw/journals/ocas-praxis/
  YYYY-MM-DD/
    {run_id}.json
```

The OCAS_ROOT environment variable overrides `~/openclaw` if set.

Default config.json:
```json
{
  "skill_id": "ocas-praxis",
  "skill_version": "2.0.0",
  "config_version": "1",
  "created_at": "",
  "updated_at": "",
  "shifts": {
    "max_active": 12
  },
  "lessons": {
    "min_pattern_count": 2
  },
  "retention": {
    "days": 0,
    "max_records": 10000
  }
}
```

## OKRs

Universal OKRs from spec-ocas-journal.md apply to all runs.

```yaml
skill_okrs:
  - name: shift_traceability
    metric: fraction of active shifts with at least one traced event
    direction: maximize
    target: 1.0
    evaluation_window: 30_runs
  - name: cap_compliance
    metric: fraction of runs where active shift count is at or below cap
    direction: maximize
    target: 1.0
    evaluation_window: 30_runs
  - name: lesson_precision
    metric: fraction of extracted lessons leading to activated shifts
    direction: maximize
    target: 0.50
    evaluation_window: 30_runs
  - name: debrief_quality
    metric: fraction of debriefs rated useful by human review
    direction: maximize
    target: 0.80
    evaluation_window: 30_runs
```

## Optional skill cooperation

- Corvus — receives BehavioralSignal files via intake directory
- Dispatch — receives action decisions from Praxis for communication execution

## Journal outputs

Action Journal — every event recording, lesson extraction, shift change, and debrief generation.

## Visibility

public

## Support file map

File | When to read
`references/data_model.md` | Before creating events, lessons, shifts, or debriefs
`references/lesson_rules.md` | Before extracting lessons from events
`references/runtime_rules.md` | Before generating runtime brief
`references/debrief_templates.md` | Before generating debriefs
`references/journal.md` | Before praxis.journal; at end of every run
