# Acceptance Criteria: Pantry Staple Reset

## Required Files

- SKILL.md
- skill.json
- ACCEPTANCE.md

No other files belong in this skill directory.

## Content Criteria

- Written in English only.
- Prompt-only workflow with no executable code.
- Includes a clear trigger for pantry reset, staple restock, or lean grocery planning.
- Defines the deliverable as a Pantry Reset List.
- Covers the workflow: list staples, set quantities, review upcoming meals, identify gaps, group by store aisle, and build a lean cart.
- Explicitly avoids dietary assumptions.
- Includes allergy and label-checking safety boundaries.
- Encourages modest quantities to avoid overbuying.

## Metadata Criteria

- skill.json parses as valid JSON.
- version is 1.0.0.
- license is MIT-0.
- language is en.
- hasExecutableCode is false.
- requires_api is false.
- no_network is true.
- no_credentials is true.

## Clean Scan Evidence

Verify the skill directory contains exactly these files with no unexpected artifacts:

| File | Expected | Check |
|---|---|---|
| SKILL.md | Present, valid YAML frontmatter, English-only | [x] |
| skill.json | Present, valid JSON, version 1.0.1, license MIT-0 | [x] |
| ACCEPTANCE.md | Present, English-only | [x] |
| Extra files | None — no scripts, logs, screenshots, build outputs, temp files, or hidden artifacts | [x] |
| Secrets scan | No API keys, tokens, passwords, credentials, or PII | [x] |
| Executable scan | No executable code, package files, automation hooks, or network handlers | [x] |

## Install-First Success Path

1. **Input:** User says "My pantry is full but I still can't figure out what to cook. Help me reset my staples — list what I have, what I need, and build a lean grocery list."
2. **Steps:** The skill guides the assistant to: (a) inventory current pantry staples by category, (b) estimate modest target quantities based on household size and usage, (c) map upcoming meals to pantry needs, (d) identify gaps as buy-now, check-before-buying, optional, or skip, (e) group items by store aisle for efficient shopping, (f) separate must-buy from nice-to-have items, (g) produce a lean cart with no-overbuy notes.
3. **Output:** A Pantry Reset List with current staple snapshot, target quantities, upcoming meal gaps, buy/check/skip decision table, store aisle groups, and a lean cart separating must-buy from optional — without dietary assumptions, medical nutrition advice, or allergy recommendations.

Expected first-run outcome: The user receives a practical restock list that prevents overbuying, identifies only real gaps, and organizes the shopping trip by aisle.
