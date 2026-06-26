# LessonLoop

A lightweight self-improvement skill for OpenClaw agents.

This project is **LessonLoop**.

## What it does

LessonLoop turns important user feedback into durable behavior changes without expensive every-turn reflection.

It is designed for one goal:

**Capture only high-value lessons, compress them, and apply them with minimal token overhead.**

## Core idea

Most self-improving agent systems burn too many tokens because they reflect too often.

LessonLoop uses a lighter design:
- event-triggered capture instead of continuous reflection
- compressed lessons instead of long summaries
- daily-memory write first, long-term promotion only when justified
- local/Ollama first-pass where possible
- stronger model only for ambiguous or high-stakes cases

## Best use cases

- user corrections
- new operating rules
- repeated mistakes
- explicit "remember this" instructions
- hardening preferences and workflows over time

## Included scripts

- `scripts/apply_lesson.py` — write a compact lesson to daily memory and log the event in one step
- `scripts/capture_lesson.py` — append a compact lesson to daily memory
- `scripts/lesson_gate.py` — decide whether a lesson needs escalation
- `scripts/log_lesson_event.py` — record structured LessonLoop events for evaluation
- `scripts/lessonloop_report.py` — generate a compact LessonLoop status/report

## Included references

- `references/lesson-types.md`
- `references/ollama-pass-template.md`
- `references/status-format.md`

## Why it matters

LessonLoop is not trying to make a model smarter in the abstract.
It is trying to make real usage compound over time.

## Current maturity

LessonLoop is in internal trial stage.

It is already runnable and useful, but still needs real-world observation around:
- trigger accuracy
- lesson quality
- false positives
- memory bloat
- actual reduction in repeated mistakes

## Product direction

- low-token self-improvement
- local-first lesson triage
- durable rule capture without reflection spam

## License

MIT-0
