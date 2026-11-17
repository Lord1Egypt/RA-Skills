# Contributing to humanize-text-skill

Thanks for helping. `humanize-text-skill` is a bilingual AI-writing skill that removes AI-shaped prose and pulls clean drafts toward a target human voice.

## Ground rules

- Keep the public contract aligned across `README.md`, `SKILL.md`, `detector/CATEGORIES.md`, and `policy/`.
- Do not change scoring semantics casually. `score`, `fidelity`, and `voice.drift` are separate by design.
- Prefer data-backed policy changes in `policy/*.toml` over buried prose changes.
- Preserve protected spans and do not weaken the false-positive guardrails.

## Before you open a change

- run `npm test`
- review `scripts/check-counts.sh`
- review `scripts/check-policy.js`
- confirm any new detector `type` is documented in `detector/CATEGORIES.md`

## Terminology

- **Tier**: how strongly a pattern signals AI-shaped prose
- **Scene**: where the text will ship and how much intervention it can tolerate
- **Voice mode**: the target voice pull applied after subtraction

## Design sources

`humanize-text-skill` stands on:

- [`avoid-ai-writing`](https://github.com/conorbronsdon/avoid-ai-writing)
- [`shuorenhua`](https://github.com/MrGeDiao/shuorenhua)
