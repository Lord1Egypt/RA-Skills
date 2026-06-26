# Acceptance Criteria - Home Noise Evidence Log

## Gate Checks

- [x] `SKILL.md` exists and contains a prompt-only workflow.
- [x] `skill.json` is valid JSON and declares `version=1.0.0`, `license=MIT-0`, `language=en`, and `hasExecutableCode=false`.
- [x] File count is exactly 3: `SKILL.md`, `skill.json`, and `ACCEPTANCE.md`.
- [x] Public-facing documentation is English only.
- [x] No executable code, scripts, package files, network calls, APIs, credentials, secrets, or private data are included.
- [x] Trigger scenario, concrete deliverable, workflow, output format, and safety boundary are explicit.
- [x] The workflow produces a noise issue snapshot, timestamped incident log, proof index, pattern summary, gaps list, neutral message draft, follow-up tracker, and packaging checklist.
- [x] The skill stays within calm documentation and neutral communication.
- [x] The skill avoids legal advice, tenant-rights advice, confrontation coaching, threats, retaliation, surveillance, and fabricated evidence.
- [x] The safety boundary routes threats, violence, stalking, property damage, or immediate danger to local emergency or qualified support.
- [x] No CJK characters are present.

## Clean Scan Evidence

Verify the skill directory contains exactly these files with no unexpected artifacts:

| File | Expected | Check |
|---|---|---|
| SKILL.md | Present, English, YAML frontmatter with name/description | ✅ |
| skill.json | Valid JSON, version 1.0.0, license MIT-0, language en, hasExecutableCode false | ✅ |
| ACCEPTANCE.md | Present, English, gate checks documented | ✅ |
| Extras | No executable scripts, package files, .env, credentials, logs, temp files, or network configs | ✅ |

Scan command: `find . -type f | sort` → exactly 3 files.

## Install-First Success Path

1. **Input:** User says "My upstairs neighbor is loud every night. Help me make a calm noise log."
2. **Steps:** The skill guides the assistant to: (a) set scope and safety note, (b) define the noise issue neutrally, (c) create a timestamped incident log, (d) index user-provided proof, (e) summarize the pattern, (f) flag gaps, (g) check official process if supplied, (h) draft a neutral message, (i) add a follow-up tracker.
3. **Output:** A documentation packet with noise issue snapshot, timestamped incident log, proof index, pattern summary, gaps list, neutral message draft, follow-up tracker, and packaging checklist. The user can immediately send the neutral message or file the log.

Expected first-run outcome: The user has a calm, factual noise log they can share with management, an HOA, a landlord, or a neighbor without escalation.

## Scope

- Prompt-only MVP.
- Local implementation only.
- Not published to ClawHub in this phase.

## Review Status

- Implemented by: Golden Bean / coder
- Date: 2026-05-11
- Status: Ready for cross-review and test.
