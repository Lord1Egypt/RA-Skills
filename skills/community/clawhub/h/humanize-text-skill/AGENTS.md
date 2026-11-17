# AGENTS.md

`humanize-text-skill` is a bilingual AI-writing skill for two linked tasks:

- subtraction: remove AI-shaped tone and templated phrasing
- addition: pull the result toward a target human voice

The project combines the engineering discipline of `avoid-ai-writing` with the Chinese coverage depth inspired by `shuorenhua`.

## Repository layout

- `SKILL.md` is the single rule entry point and mode contract.
- `detector/` contains the zero-dependency engine for Node `>=18` and browser use.
- `references/` stores the human-readable rule source.
- `policy/` stores scene, tier, and voice policy as auditable `.toml` data.
- `evals/` stores benchmark cases, fixtures, and voice samples.
- `plugins/`, `cursor-rules/`, and `install/` hold platform packaging and setup guidance.

## Non-drifting contracts

1. One scorer: `score` is computed only in `detector/core/scoring.js`. `fidelity` is a gate, not a score. `voice.drift` is independent.
2. Count consistency: the README pattern-category count must match the detectable `###` count in `SKILL.md`, and every detector `type` must be documented in `detector/CATEGORIES.md`.
3. Policy alignment: names referenced in `policy/*.toml` must exist in engine enums, and `matrix.toml` must cover every scene-by-tier cell.

## Modes

`rewrite` is the default mode. `detect` audits without rewriting. `edit` performs minimal in-place changes. Every mode runs protected-span detection first. Any `voiceMode` other than `none` enables voice-pull suggestions.

## Related work

- `avoid-ai-writing` by conorbronsdon
- `shuorenhua` by MrGeDiao
