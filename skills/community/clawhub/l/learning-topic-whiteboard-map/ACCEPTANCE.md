# Acceptance Criteria - Learning Topic Whiteboard Map

## Gate Checks

- [x] `SKILL.md` exists and contains a prompt-only workflow.
- [x] `skill.json` is valid JSON and declares `version=1.0.0`, `license=MIT-0`, `language=en`, and `hasExecutableCode=false`.
- [x] File count is exactly 3: `SKILL.md`, `skill.json`, and `ACCEPTANCE.md`.
- [x] Public-facing documentation is English only.
- [x] No executable code, scripts, package files, network calls, APIs, credentials, secrets, or private data are included.
- [x] Trigger scenario, concrete deliverable, workflow, output format, and safety boundary are explicit.
- [x] The workflow supports naming the topic, breaking it into modules, adding examples, placing practice tasks, marking confidence, labeling uncertainty, and choosing next study actions.
- [x] The deliverable is a visible whiteboard or wall-ready map rather than a generic study plan.
- [x] The skill labels uncertain sources, user-provided claims, missing citations, and source-dependent content.
- [x] The skill avoids credential claims and avoids medical, legal, financial, or professional advice claims.
- [x] No CJK characters are present.

## Scope

- Prompt-only MVP.
- Local implementation only.
- Not published to ClawHub in this phase.

## Clean Scan Evidence

Verify the skill directory contains exactly these files with no unexpected artifacts:

| File | Expected | Check |
|---|---|---|
| SKILL.md | Present, English, YAML frontmatter with name/description | ✅ |
| skill.json | Valid JSON, version 1.0.1, license MIT-0, language en, hasExecutableCode false | ✅ |
| ACCEPTANCE.md | Present, English, gate checks documented | ✅ |
| Extras | No executable scripts, package files, .env, credentials, logs, temp files, or network configs | ✅ |

Scan command: `find . -type f | sort` → exactly 3 files.

## Install-First Success Path

1. **Input:** User says "I'm learning linear algebra for machine learning and it feels like a wall of formulas. Build me a whiteboard map so I can see how the topics connect and where I need more practice."
2. **Steps:** The skill guides the assistant to: (a) define one clear topic title and target outcome, (b) break the topic into 4–8 modules with prerequisite ordering, (c) add concept links with relationship labels (depends on, contrasts with, example of), (d) attach one concrete example or mini-case to each module, (e) add practice tasks matched to the user's level, (f) mark confidence with green/yellow/red/gray status, (g) label uncertain sources and unsourced claims, (h) pick the next 3 study actions and a maintenance rule.
3. **Output:** A Learning Topic Whiteboard Map card with topic target, board legend, module map table, concept links table, examples and practice table, uncertain sources and claims table, next study actions, and a maintenance rule — all designed to transfer to a whiteboard or sticky-note grid.

Expected first-run outcome: The user receives a visible study map that turns a confusing wall of material into ordered modules with examples, confidence marks, and clear next actions — without credential claims or unsourced assertions.

## Review Status

- Implemented by: Golden Bean / coder
- Date: 2026-05-11
- Status: Ready for cross-review and test.
