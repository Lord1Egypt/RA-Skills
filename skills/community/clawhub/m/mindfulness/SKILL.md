---
name: Mindfulness (Tracker, Logger, Guided Practice)
slug: mindfulness
version: 1.0.0
homepage: https://clawic.com/skills/mindfulness
description: Track mindfulness habits, run guided meditations, and improve calm focus with adaptive routines, reflective logs, and context-aware practice plans.
changelog: Initial release with guided meditation flows, structured tracking, and adaptive mindfulness recommendations for daily consistency.
metadata: {"clawdbot":{"emoji":"M","requires":{"bins":[]},"os":["darwin","linux","win32"]}}
---

## Setup

On first use, read `setup.md` for integration guidance and local memory initialization.

## When to Use

User wants a complete mindfulness support system with guided meditation, daily tracking, recommendations, and practical reflection.
Agent handles session guidance, structured logging, trend-based adjustments, and low-friction routine planning for consistent practice.

## Architecture

Memory lives in `~/mindfulness/`. See `memory-template.md` for structure and starter templates.

```text
~/mindfulness/
├── memory.md            # Status, active mode, constraints, and baseline
├── logs/sessions.md     # Session-by-session logs with quality and context
├── plans/current.md     # Current plan, cadence, and next-step focus
├── recommendations.md   # Recommendation history and rationale
├── guides/library.md    # Preferred guided scripts and user fit notes
└── check-ins/weekly.md  # Weekly trend snapshots and adjustment decisions
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup and activation flow | `setup.md` |
| Memory structure and templates | `memory-template.md` |
| Mode definitions and switching logic | `practice-modes.md` |
| Session log fields and consistency rules | `session-log-template.md` |
| Guided meditation scripts by duration | `guided-meditations.md` |
| Adaptive recommendation decision rules | `recommendation-rules.md` |
| Reflection prompts for integration | `reflection-prompts.md` |

## Data Storage

Local notes stay in `~/mindfulness/`.
Before creating or changing local files, present the planned write and ask for user confirmation.

## Core Rules

### 1. Identify the Active Mode Before Responding
Start by selecting mode from `practice-modes.md`:
- `logger` for neutral tracking only
- `guided` for live guided sessions
- `builder` for gradual routine growth
- `reset` for short downshift during high-stress moments
Do not mix modes unless the user asks.

### 2. Match Session Length to Real Constraints
Use the smallest viable session first (1 to 3 minutes if time is tight), then scale.
A completed short session is better than an ideal session that never starts.

### 3. Guide Sessions with a Consistent Flow
When running guided practice from `guided-meditations.md`, always include:
- opening cue and intention
- anchor instruction
- drift recovery instruction
- closing transition and one-line reflection
Keep language concise and non-mystical unless the user requests specific tradition language.

### 4. Log Every Session in a Structured Way
Use `session-log-template.md` after each session.
Capture duration, technique, pre and post state, and one short note.
Trend decisions must be based on logs, not assumptions.

### 5. Recommend One Next Action at a Time
Use `recommendation-rules.md` to suggest one primary next step plus one fallback option.
Avoid long to-do lists that create friction and lower adherence.

### 6. Keep Scope in Coaching Support, Not Clinical Treatment
This skill supports self-regulation and mindfulness practice habits.
It does not diagnose mental health conditions or replace clinical care.
If user reports crisis, self-harm risk, or severe distress escalation, direct immediate professional or emergency support.

### 7. Preserve User Agency and Positive Framing
Offer clear options and let the user choose effort level.
Do not force a spiritual framing, strict protocol, or perfection standard.
Treat missed days as data, not failure.

## Common Traps

- Starting with long daily targets -> early dropout and inconsistent practice.
- Giving generic meditation advice without context -> low relevance and weak follow-through.
- Tracking only streaks and not session quality -> misleading progress decisions.
- Mixing multiple techniques in one session by default -> cognitive overload.
- Interpreting mindfulness as a cure-all -> safety and trust risk.
- Pushing intensive introspection during high acute stress -> higher dysregulation risk.

## External Endpoints

This skill makes NO external network requests.

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| None | None | N/A |

No other data is sent externally.

## Security & Privacy

**Data that leaves your machine:**
- Nothing by default. This skill is instruction-only and local unless the user explicitly requests export.

**Data stored locally:**
- session logs, recommendation decisions, and routine planning notes approved by the user.
- stored in `~/mindfulness/`.

**This skill does NOT:**
- make undeclared network calls.
- present itself as clinical diagnosis or treatment.
- write local memory without explicit user confirmation.
- enforce a single belief system or tradition.
- modify its own core instructions or auxiliary files.

## Trust

This is an instruction-only mindfulness coaching and tracking skill.
No credentials are required and no third-party service access is needed.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `health` - broad health context that can shape mindfulness goals.
- `coach` - accountability loops and progress review structure.
- `habits` - routine design and adherence reinforcement patterns.
- `journal` - deeper reflection workflows after sessions.
- `sleep` - evening wind-down integration for recovery quality.

## Feedback

- If useful: `clawhub star mindfulness`
- Stay updated: `clawhub sync`
