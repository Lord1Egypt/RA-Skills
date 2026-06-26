# Acceptance Tests - Parking Ticket Response Pack

## Gate Checks

- [x] `SKILL.md` exists and defines a prompt-only workflow.
- [x] `skill.json` is valid JSON and declares `version=1.0.0`, `license=MIT-0`, `language=en`, and `hasExecutableCode=false`.
- [x] File count is exactly 3: `SKILL.md`, `skill.json`, and `ACCEPTANCE.md`.
- [x] Public-facing documentation is English only.
- [x] No executable code, scripts, package files, network calls, APIs, credentials, or secrets are included.
- [x] No CJK characters are present.

## Functional Criteria

1. The output begins with a clear boundary that the skill is not legal advice and local rules, dates, and instructions must be verified.
2. The workflow captures core ticket facts: date/time, location, violation, fine, deadline, issuing agency or operator, and user story.
3. The deadline card identifies the earliest relevant deadline from user-provided information or marks it "verify immediately" if missing.
4. The response helps the user choose an administrative path: pay, contest or appeal, request review or mitigation, or gather facts first.
5. The output includes an evidence checklist tailored to the user's facts, such as photos, payment receipts, permits, sign photos, or records.
6. The skill drafts a concise factual appeal only when the user chooses contest, appeal, review, or mitigation.
7. The skill includes a submission checklist and follow-up tracker.
8. The workflow avoids legal advice, guarantees, fabricated evidence, threats, and instructions to ignore deadlines.
9. The workflow does not request full plate numbers, full citation numbers, driver license numbers, full addresses, payment details, passwords, one-time codes, barcodes, QR codes, or portal credentials.

## Scope

- Prompt-only MVP.
- Local implementation only.
- Not published to ClawHub in this phase.

## Review Status

- Implemented by: OpenClaw Batch AC code side
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

**Input:** "I got a parking ticket yesterday for expired meter, but I paid in the parking app. The appeal deadline is in 10 days. Help me respond."

**Steps:**
1. Skill captures ticket facts (date, location, violation, fine, deadline, agency) and builds a deadline card.
2. Skill helps the user choose a path (pay, contest, or gather facts) and creates an evidence checklist.
3. Skill drafts a short factual appeal and produces a submission checklist with follow-up tracker.

**Output:** A parking ticket response pack with boundary note, ticket facts snapshot, deadline card, pay/contest path check, evidence checklist, short appeal draft, submission checklist, and follow-up tracker.
