# Acceptance Criteria - Migraine Trigger Pattern Log

## Gate Checks

- [x] `SKILL.md` exists and contains a prompt-only workflow.
- [x] `skill.json` is valid JSON and declares `version=1.0.0`, `license=MIT-0`, `language=en`, and `hasExecutableCode=false`.
- [x] File count is exactly 3: `SKILL.md`, `skill.json`, and `ACCEPTANCE.md`.
- [x] Public-facing documentation is English only.
- [x] No executable code, scripts, package files, network calls, APIs, credentials, secrets, or private data are included.
- [x] Trigger scenario, concrete deliverable, workflow, output format, and safety boundary are explicit.
- [x] The workflow produces an episode log, context checklist, pattern review, clinician-friendly summary, weekly review prompt, and open questions.
- [x] The skill avoids diagnosis, treatment advice, medication changes, dose recommendations, and medical certainty.
- [x] The safety boundary flags severe sudden headache, neurological symptoms, fever, injury, pregnancy concerns, vision loss, new or worsening patterns, and other alarming symptoms for urgent or professional care.
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

- SKILL.md: English only, no CJK/non-ASCII characters, no secrets, no credentials, no API keys, no tokens, no passwords, no personal data.
- skill.json: valid JSON, English only, all required safety fields present (hasExecutableCode: false, requires_api: false, no_network: true, no_credentials: true, no_code_execution: true).
- ACCEPTANCE.md: English only, no secrets, no executable content.
- Directory: exactly 3 files (SKILL.md, skill.json, ACCEPTANCE.md). No package files, scripts, binaries, .env, .git, node_modules, or hidden configs.
- No executable code, no network calls, no API dependencies, no credential requirements.

## Install-First Success Path

1. **Input:** User describes recurring headache episodes with dates, severity, symptoms, possible context factors, and any medications or interventions used.
2. **Steps:** Skill checks for urgent red flags first, defines the tracking goal, records each episode with date/time/severity/symptoms/context, captures possible trigger factors, tracks interventions and response, reviews patterns cautiously without claiming causation, and creates a clinician-friendly appointment summary.
3. **Output:** A migraine pattern log package with episode log template, context checklist, pattern review table, clinician-friendly summary, weekly review prompt, and open questions list.
