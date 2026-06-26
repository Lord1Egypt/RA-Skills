# Evals for nail-b3g1-promo

Test prompts in `evals.json` follow [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) schema and are used to verify the skill produces B3G1 rule definition, automation guidance, copy, and metrics.

## evals.json structure (skill-creator compliant)

- **skill_name**: `nail-b3g1-promo` (matches SKILL.md frontmatter `name`)
- **evals**: array; each item has
  - **id**: unique integer
  - **prompt**: user task (realistic scenario)
  - **expected_output**: short description of expected result
  - **files**: input file paths relative to skill root (e.g. `evals/files/...`), or `[]`
  - **expectations**: list of verifiable statements (strings); grader uses these and writes `grading.json` with `text`, `passed`, `evidence` per expectation

## Eval coverage

1. **Eval 1** — Nail polish (cat-eye, matte) B3G1, Shopify: rule, automation, PDP and cart copy, scope = nail polish collection.
2. **Eval 2** — Press-on B3G1, cart auto-apply, Rijoy user: rule, cart automation, Rijoy/loyalty note.
3. **Eval 3** — Weekend-only B3G1, gel-effect, exclude new launch: rule with exclusions, time trigger, banner copy.

## Workspace and iterations

Per skill-creator: put run results in a workspace **sibling** to the skill directory, e.g. `nail-b3g1-promo-workspace/`, under `iteration-N/<eval_name>/` with `with_skill/`, `without_skill/` (or baseline), `eval_metadata.json`, and after grading: `grading.json`, `timing.json`. Use `scripts.aggregate_benchmark` and `eval-viewer/generate_review.py` from the skill-creator skill to produce `benchmark.json` and the review viewer.
