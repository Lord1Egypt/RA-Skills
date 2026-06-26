---
name: Pregnancy (Tracker, Journal, Triage, Visit Prep)
slug: pregnancy
version: 1.0.0
homepage: https://clawic.com/skills/pregnancy
description: Track pregnancy routines, symptoms, and clinical signals with flexible logs, weekly summaries, and safety-first triage for medical follow-up.
changelog: Initial release with flexible pregnancy tracking modules, clinician-ready weekly summaries, and safety triage guardrails.
metadata: {"clawdbot":{"emoji":"P","requires":{"bins":[]},"os":["darwin","linux","win32"]}}
---

## Setup

On first use, read `setup.md` for integration guidance and local memory initialization.

## When to Use

User wants a flexible pregnancy tracker for symptoms, routines, medications, appointments, questions, or warning signs.
Agent structures logs, keeps data clinically useful, and prepares concise summaries for prenatal visits without replacing medical care.

## Architecture

Memory lives in `~/pregnancy/`. See `memory-template.md` for structure and starter templates.

```text
~/pregnancy/
|-- memory.md                 # Status, context, and active tracking modules
|-- logs/daily-log.md         # Day-by-day entries with timestamps and units
|-- summaries/weekly.md       # Weekly clinical summary and trend notes
|-- summaries/visit-prep.md   # Questions and priorities for the next appointment
|-- alerts/events.md          # Red and amber events with trigger reasons
`-- preferences/thresholds.md # User-specific tracking scope and escalation choices
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup and activation behavior | `setup.md` |
| Memory structure and templates | `memory-template.md` |
| Flexible tracking framework | `tracking-framework.md` |
| Metric catalog and units | `metric-catalog.md` |
| Data quality and validation rules | `data-quality.md` |
| Red and amber triage rules | `triage-rules.md` |
| Weekly and visit summary format | `visit-summary-template.md` |

## Data Storage

Local notes stay in `~/pregnancy/`.
Before creating or changing local files, present the planned write and ask for user confirmation.

## Core Rules

### 1. Define Scope Before Logging
Start with user intent and care context:
- basic wellness tracking only
- clinician-facing pregnancy tracking
- high-risk monitoring support
Enable only modules the user wants, then expand gradually.

### 2. Keep Tracking Flexible but Structured
Use `tracking-framework.md` to run modular tracking:
- core daily block for minimum continuity
- optional blocks for symptoms, medications, appointments, mood, sleep, nutrition, fetal movement, or glucose
- custom user-defined blocks when needed
Do not force all modules at once.

### 3. Preserve Clinical Utility of Data
Use `metric-catalog.md` and `data-quality.md`:
- always record timestamp, unit, and context
- normalize values to one unit system
- separate observed facts from interpretation
Reject ambiguous entries and ask for missing context.

### 4. Generate Visit-Ready Summaries
At least weekly, generate a concise summary using `visit-summary-template.md`:
- trend overview
- out-of-range or concerning events
- unresolved questions for clinician
Keep summaries short enough for prenatal visit use.

### 5. Apply Safety-First Triage
Use `triage-rules.md` for red and amber conditions.
If emergency signs appear, provide immediate emergency guidance first.
Do not continue routine coaching before urgent escalation guidance.

### 6. Stay in Support Scope, Not Diagnosis Scope
This skill supports organization, tracking, and escalation cues.
It does not diagnose, prescribe, interpret imaging, or replace clinician judgment.
For medication changes or treatment decisions, route user to their care team.

### 7. Protect Privacy and User Agency
Track only pregnancy-relevant information needed for user goals.
Offer opt-in detail levels and allow pause, simplify, or delete requests.
Never add hidden background tracking.

## Common Traps

- Logging too much too soon -> dropout and inconsistent data quality.
- Missing timestamps or units -> trends become unreliable for clinicians.
- Mixing reassurance with warning signs -> delayed urgent care.
- Treating optional consumer metrics as clinical truth -> noisy decisions.
- Summaries with raw dumps only -> poor usability during appointments.
- Giving treatment advice beyond scope -> safety and trust risk.

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
- tracking logs, weekly summaries, alert events, and clinician question lists approved by the user.
- stored in `~/pregnancy/`.

**This skill does NOT:**
- diagnose pregnancy conditions or provide emergency medical treatment.
- make undeclared network calls.
- modify files without explicit user confirmation.
- collect unrelated personal data.

## Trust

This is an instruction-only pregnancy tracking and visit-prep skill.
No credentials are required and no third-party service access is needed.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `health` - general health planning and longitudinal habit support.
- `doctor` - structured preparation for medical consultations and follow-up.
- `symptoms` - focused symptom capture and pattern tracking workflows.
- `nutrition` - meal and hydration planning aligned with health goals.
- `sleep` - sleep routines and recovery support for energy management.

## Feedback

- If useful: `clawhub star pregnancy`
- Stay updated: `clawhub sync`
