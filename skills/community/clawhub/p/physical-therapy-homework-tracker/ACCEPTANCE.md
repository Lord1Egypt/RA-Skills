# Acceptance Criteria - Physical Therapy Homework Tracker

## Gate Checks

- [x] `SKILL.md` exists and contains a prompt-only workflow.
- [x] `skill.json` is valid JSON and declares `version=1.0.0`, `license=MIT-0`, `language=en`, and `hasExecutableCode=false`.
- [x] File count is exactly 3: `SKILL.md`, `skill.json`, and `ACCEPTANCE.md`.
- [x] Public-facing documentation is English only.
- [x] No executable code, scripts, package files, network calls, APIs, credentials, secrets, or private data are included.
- [x] Trigger scenario, concrete deliverable, workflow, output format, and safety boundary are explicit.
- [x] The workflow produces a PT homework tracker with prescribed-exercise table, weekly adherence log, symptom response notes, modification questions, appointment update brief, and red-flag reminder.
- [x] The skill is differentiated from general fitness, workout planning, injury diagnosis, and rehabilitation protocol design by only organizing a user-provided clinician-prescribed plan.
- [x] The skill avoids medical advice, diagnosis, treatment, exercise prescription, intensity changes, and encouragement to continue through pain.
- [x] No CJK characters are present.

## Scope

- Prompt-only MVP.
- Local implementation only.
- Not published to ClawHub in this phase.

## Review Status

- Implemented by: Golden Bean / coder
- Date: 2026-05-10
- Status: Ready for cross-review and test.

## Clean Scan Evidence

- [x] No executable code, scripts, binaries, or package files.
- [x] No secrets, credentials, API keys, tokens, or environment variables.
- [x] No network calls, API endpoints, or internet dependencies.
- [x] No CJK characters. Documentation is English/ASCII only.
- [x] `skill.json` is valid JSON with `version=1.0.0`, `license=MIT-0`, `language=en`, `hasExecutableCode=false`.
- [x] File count is exactly 3: `SKILL.md`, `skill.json`, `ACCEPTANCE.md`.
- [x] No temp files, log files, or build artifacts.

## Install-First Success Path

**Input:** "My PT gave me five knee exercises and I keep forgetting them. Build a tracker."

**Steps:**
1. Skill asks for prescribed exercises (sets, reps, frequency, equipment, precautions) and appointment details.
2. Skill guides the user through organizing exercises into a daily/weekly checklist with adherence logs.
3. Skill helps the user record symptom observations (pain, mobility, confidence) and draft appointment questions.

**Output:** A PT homework tracker with prescribed-exercise table, weekly adherence log, symptom notes, appointment update brief, and red-flag reminder — all organized from user-provided clinician instructions.
