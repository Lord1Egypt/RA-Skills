---
name: Pilates (Session Planner, Form Coach, Progress Tracker)
slug: pilates
version: 1.0.0
homepage: https://clawic.com/skills/pilates
description: Plan Pilates sessions, refine form, and track steady progress with equipment-aware modifications, core-focused cues, and weekly reviews.
changelog: Initial release with session planning, form repair workflows, equipment-aware modifications, and weekly progression reviews.
metadata: {"clawdbot":{"emoji":"P","requires":{"bins":[]},"os":["darwin","linux","win32"],"configPaths":["~/pilates/"]}}
---

## When to Use

User wants Pilates support for mat practice, reformer-informed home work, posture and control drills, recovery-minded training, or a consistent core-focused routine.
Agent helps choose the right session mode, build realistic blocks, fix one form issue at a time, and keep safety boundaries visible.

## Architecture

Memory lives in `~/pilates/`. If `~/pilates/` does not exist, run `setup.md`. See `memory-template.md` for structure and starter templates.

```text
~/pilates/
|-- memory.md                    # Status, current goals, equipment context, and practice cadence
|-- sessions/log.md              # Session-by-session log with duration, mode, and key notes
|-- plans/current-plan.md        # Active weekly plan and next session target
|-- form/checkpoints.md          # Recurring alignment issues and correction cues
|-- summaries/weekly-review.md   # Weekly trend snapshot and next-step decisions
`-- safety/modifications.md      # User-specific limits, stop signals, and approved adjustments
```

## Quick Reference

Use these files as operating modules. Load the smallest file that matches the current coaching job.

| Topic | File |
|-------|------|
| Setup and activation behavior | `setup.md` |
| Memory structure and templates | `memory-template.md` |
| Mode selection and switching | `practice-modes.md` |
| Session blueprints by duration | `session-templates.md` |
| Form checks and coaching cues | `form-checks.md` |
| Safety boundaries and modifications | `safety-modifications.md` |
| Progression rules and weekly review | `progression-ladder.md` |
| Personal practice review prompts | `weekly-review-template.md` |

## Data Storage

Local notes stay in `~/pilates/`.
Before creating or changing local files, present the planned write and ask for user confirmation.

## Core Rules

### 1. Choose the Right Practice Mode First
Use `practice-modes.md` before suggesting anything:
- `start` for first sessions, inconsistent practice, or low body awareness
- `session` for normal guided Pilates work
- `repair` for fixing one specific form issue
- `build` for weekly progression and consistency
- `recover` for lower-intensity practice when pain, fatigue, or confidence limits are active
Do not mix multiple goals unless the user explicitly wants a blended session.

### 2. Keep Sessions Small, Precise, and Repeatable
Use `session-templates.md` to match the user's real constraints:
- 5 to 8 minutes for consistency rescue
- 10 to 20 minutes for most home sessions
- longer sessions only when adherence and form control are already stable
Default to the smallest useful session the user is likely to repeat.

### 3. Coach Through the Stack-Brace-Breathe Loop
When giving live cues or post-session corrections, use this order:
- **Stack**: ribs over pelvis, neck long, shoulders organized
- **Brace**: light abdominal support without gripping or breath holding
- **Breathe**: steady inhale and exhale that match the movement
Use `form-checks.md` to correct one pattern at a time, not the whole body at once.

### 4. Match the Drill to the Equipment and Experience
A mat beginner, a reformer regular, and a low-back-sensitive user do not need the same cues.
Use props, wall support, or smaller ranges before increasing difficulty.
If the user references studio work, translate the intent of the exercise rather than pretending to recreate every machine exactly.

### 5. Separate Practice Goals from Health Claims
This skill supports movement quality, control, consistency, posture awareness, and structured habit building.
It does not diagnose injuries, promise rehabilitation outcomes, or replace clinician or instructor judgment.
If the user has pregnancy concerns, recent surgery, persistent numbness, major pain flare-ups, or bone-health restrictions, use `safety-modifications.md` and keep escalation thresholds explicit.

### 6. Track Only the Signals That Change Decisions
Use `memory-template.md`, `progression-ladder.md`, and `weekly-review-template.md` to capture:
- practice frequency
- exercise tolerance
- quality of breathing and control
- recurring pain or stop signals
- the main form priority for the next week
Do not over-log details that do not improve the next session.

### 7. End Every Session with One Correction and One Win
Every guided session or review should end with:
- one primary correction cue
- one confirmed strength or improvement
- one concrete next session target
Too many corrections reduce confidence and make technique worse.

## Common Traps

- Treating Pilates like a burn-more workout instead of a control practice -> speed replaces precision.
- Using advanced exercise names without checking the user's experience -> confusion and poor adherence.
- Correcting breathing, ribs, pelvis, neck, and pace all at once -> overload and lower body awareness.
- Copying reformer intensity onto mat work without context -> poor exercise selection.
- Forcing neutral spine as a rigid rule in every drill -> unnecessary tension and weaker movement quality.
- Claiming Pilates will fix pain or posture automatically -> unsafe expectations and trust loss.
- Logging every rep but never reviewing patterns -> no real progression decisions.

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
- session logs, practice plans, form checkpoints, and safety notes approved by the user.
- stored in `~/pilates/`.

**This skill does NOT:**
- make undeclared network calls.
- diagnose, prescribe, or replace medical or rehabilitation care.
- write local memory without explicit user confirmation.
- promise a fixed therapeutic outcome from Pilates practice.
- pretend that home equipment matches studio equipment when it does not.

## Trust

This is an instruction-only Pilates practice and tracking skill.
No credentials are required and no third-party service access is needed.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `health` - broader health context and safety-aware habit framing.
- `fitness` - general training planning and consistency support.
- `yoga` - adjacent breath, posture, and mobility language for crossover users.
- `mindfulness` - calm focus and body-awareness routines that pair well with Pilates.
- `habits` - behavior design for making short sessions repeatable.

## Feedback

- If useful: `clawhub star pilates`
- Stay updated: `clawhub sync`
