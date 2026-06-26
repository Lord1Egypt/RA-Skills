---
name: oejts-personality-tuner
description: Administer and score the Open Extended Jungian Type Scales (OEJTS 1.2), map results to MBTI-style interaction preferences, and propose/apply personality-aware tuning updates to USER.md and SOUL.md. Use when a user asks to run a Myers-Briggs-like test, calculate type from OEJTS responses, or tune assistant behavior to a personality profile.
---

# OEJTS Personality Tuner

Use this skill to run the OEJTS 1.2 assessment, compute type results, and convert the outcome into concrete assistant behavior preferences.

## Quick Start

- Show questionnaire:
  - `python3 scripts/oejts_tuner.py template --format markdown`
- Score answers:
  - `python3 scripts/oejts_tuner.py score --answers-json '{"Q1":3,...,"Q32":4}'`
- Generate proposed updates for workspace files:
  - `python3 scripts/oejts_tuner.py apply --workspace /path/to/workspace --answers-json '{...}' --dry-run`
- Apply updates:
  - `python3 scripts/oejts_tuner.py apply --workspace /path/to/workspace --answers-json '{...}'`

## Workflow

1. Administer OEJTS 1.2 using `template` output from the script.
2. Collect 1–5 answers for `Q1..Q32`.
3. Run `score` to compute `IE`, `SN`, `FT`, `JP`, type letters, and confidence.
4. Run `apply --dry-run` to preview USER.md/SOUL.md changes.
5. Confirm with user, then run `apply` without `--dry-run`.

## Rules

- Use OEJTS type as a **preference signal**, not fixed identity.
- Prefer adjustable behavior vectors over stereotypes.
- Keep user override available (user feedback beats test output).
- Preserve existing USER.md/SOUL.md content; append/update only the managed blocks.

## Managed Blocks

This skill writes only between these markers:

- USER.md:
  - `<!-- OJTS_PROFILE_START -->`
  - `<!-- OJTS_PROFILE_END -->`
- SOUL.md:
  - `<!-- OJTS_ADAPTATION_START -->`
  - `<!-- OJTS_ADAPTATION_END -->`

If blocks do not exist, they are appended.

## References

- `references/oejts-1.2.md` — canonical OEJTS items and scoring equations.
- `references/behavior-mapping.md` — type-to-behavior mapping and adaptive guidance.
