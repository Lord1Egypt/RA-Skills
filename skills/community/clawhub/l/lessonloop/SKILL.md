---
name: lessonloop
description: Lightweight experience-capture and behavior-hardening for Goat. Use when the user explicitly gives corrective feedback, says to remember or avoid something, approves a new operating rule, points out a repeated mistake, or asks Goat to improve itself without adding high token overhead. This skill records only high-value lessons, promotes durable rules into MEMORY.md when justified, and avoids verbose self-reflection loops.
---

# LessonLoop

## Overview

Use this skill to convert important feedback into durable behavior changes with minimal token cost. Prefer event-triggered capture over continuous self-reflection.

## Core rule

Do **not** run broad self-analysis. Only act when at least one of these is true:

- The user explicitly says "remember", "以后", "别再", "固定下来", "写进记忆", or similar
- The user corrects a mistake or rejects an output pattern
- A new operating rule is agreed
- A repeated failure should become a hard constraint

If none apply, do not use this skill.

## Workflow

### 0. Use the low-cost decision path first

Prefer a two-layer path:

1. **Local/Ollama first-pass** for simple classification, compression, and promotion pre-check
2. **Main model final pass** only when the case is ambiguous, strategic, or likely to affect long-term defaults

Use local/Ollama for:
- classifying feedback into a lesson type
- compressing a lesson into 1-2 lines
- deciding whether a lesson is probably daily-memory-only or a candidate for long-term promotion

Escalate to the main model only when:
- the lesson changes global operating rules
- the wording is ambiguous or high-stakes
- the summary may distort the user's intent
- the lesson affects safety, billing, routing, or durable priorities

### 1. Classify the feedback

Map the event into one of four buckets:

1. **Preference** — style, brevity, tone, output format
2. **Rule** — default behavior, routing, cost control, escalation condition
3. **Mistake** — something Goat did wrong and should avoid repeating
4. **Priority** — what to optimize first right now

### 2. Decide storage level

- Write to `memory/YYYY-MM-DD.md` for short-term events, fresh corrections, and local context
- Also update `MEMORY.md` only if the lesson is durable and should shape future sessions
- Do not promote transient details into `MEMORY.md`

### 3. Write in compressed form

Store the smallest useful rule.

Prefer:
- "Boss requires strict token-efficiency discipline"
- "Default to short answers and minimal tools"

Avoid:
- long narrative explanations
- emotional framing
- detailed postmortems unless specifically requested

### 4. Apply immediately

After writing memory, change behavior in the current session right away. Do not wait for the next session.

## Writing rules

- Keep each stored lesson to 1-2 lines
- Prefer imperative language
- Record the correction, not the whole story
- If a lesson changes defaults, phrase it as a rule
- If the user approved a protocol, name it consistently (for example: `Session throttling protocol v1`)

## Promotion guide

Promote to `MEMORY.md` when a lesson is:
- likely to matter across many sessions
- tied to cost, safety, trust, routing, or communication style
- a default operating rule

Keep only in daily memory when it is:
- temporary
- experimental
- tied to a single task
- not yet validated by repeated use or explicit user approval

## Anti-bloat guardrails

- Do not summarize every conversation
- Do not run reflection after every task
- Do not create extra memory files
- Do not duplicate the same rule in multiple places unless promoting from daily memory to long-term memory
- Do not trigger memory search unless the task actually depends on prior decisions, preferences, dates, people, or todos

## Resources

### scripts/
- `scripts/apply_lesson.py` writes a compact lesson to daily memory and logs a structured LessonLoop event in one step
- `scripts/capture_lesson.py` appends a compact lesson to the canonical daily memory file
- `scripts/log_lesson_event.py` writes structured LessonLoop event logs for evaluation and reporting
- `scripts/lessonloop_report.py` summarizes recent LessonLoop activity and outputs a compact report

### references/
- `references/lesson-types.md` contains compact classification and phrasing patterns
- `references/status-format.md` defines a compact report/status output format
