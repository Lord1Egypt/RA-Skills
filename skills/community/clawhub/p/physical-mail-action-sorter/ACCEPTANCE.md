# Acceptance Tests - Physical Mail Action Sorter

## Gate Checks

- [x] `SKILL.md` exists and defines a prompt-only workflow.
- [x] `skill.json` is valid JSON and declares `version=1.0.0`, `license=MIT-0`, `language=en`, and `hasExecutableCode=false`.
- [x] File count is exactly 3: `SKILL.md`, `skill.json`, and `ACCEPTANCE.md`.
- [x] Public-facing documentation is English only.
- [x] No executable code, scripts, package files, network calls, APIs, credentials, or secrets are included.
- [x] No CJK characters are present.

## Functional Criteria

1. The skill starts with a privacy warning not to upload or type account numbers, full IDs, payment details, passwords, one-time codes, or private case numbers.
2. The output includes a four-bin sorting card with Act Today, Review This Week, Archive, and Discard or Shred.
3. The workflow uses safe sender clues and visible envelope-level information rather than sensitive contents.
4. Each listed mail item receives a bin, reason, and action label.
5. The output includes an action tracker with item, action, due date, status, and next step.
6. The output includes discard and archive rules.
7. The workflow avoids legal, tax, medical, insurance, credit, or financial advice.
8. The workflow does not tell the user to discard official or ambiguous mail without review.

## Clean Scan Evidence

- [x] No executable code, scripts, package files, or install hooks.
- [x] No API endpoints, network calls, or external service dependencies.
- [x] No credentials, tokens, passwords, or private keys.
- [x] No secrets, environment variables, or configuration secrets.
- [x] No CJK characters; English/ASCII only.
- [x] No executable or network behavior; document-only skill.
- [x] No hidden files, temp files, or log files.
- [x] File count is exactly 3: SKILL.md, skill.json, ACCEPTANCE.md.

## Install-First Success Path

**Input:** User has a physical mail pile they want to sort and act on.

**Steps:**
1. Agent asks for safe sender clues, envelope types, and visible dates from the mail pile.
2. Agent issues a privacy reminder not to share account numbers or sensitive identifiers.
3. Agent sorts each item into one of four bins: Act Today, Review This Week, Archive, Discard or Shred.
4. Agent writes action labels and builds a tracker with due dates and next steps.
5. Agent provides discard/archive rules and a 20-minute sort plan.

**Output:** A complete mail sorting kit with a four-bin card, sorted mail board, action tracker, discard/archive rules, and a 20-minute sort plan.

## Scope

- Prompt-only MVP.
- Local implementation only.
- Not published to ClawHub in this phase.

## Review Status

- Implemented by: OpenClaw Batch AC code side
- Date: 2026-05-10
- Status: Ready for cross-review and test.
