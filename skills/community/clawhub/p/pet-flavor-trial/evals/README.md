# Evals for pet-flavor-trial

Test prompts in `evals.json` follow [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) schema and are used to verify the skill produces bundle definition, naming, copy/placement, and metrics.

## evals.json structure (skill-creator compliant)

- **skill_name**: `pet-flavor-trial` (matches SKILL.md frontmatter `name`)
- **evals**: array; each item has
  - **id**: unique integer
  - **prompt**: user task (realistic scenario)
  - **expected_output**: short description of expected result
  - **files**: input file paths relative to skill root (e.g. `evals/files/...`), or `[]`
  - **expectations**: list of verifiable statements (strings); grader uses these and writes `grading.json` with `text`, `passed`, `evidence` per expectation

## Eval coverage

1. **Eval 1** — Freeze-dried 4 flavors (chicken, beef, salmon, sweet potato): bundle table, name, PDP and cart copy, scope limited to freeze-dried.
2. **Eval 2** — Chew sticks 5 flavors, try 3–4: trial bundle definition, naming, PDP/cart, Shopify implementation note.
3. **Eval 3** — 3 flavors, no discount (margin-safe): 3-flavor bundle, same price as components, copy.

## Workspace and iterations

Per skill-creator: put run results in a workspace **sibling** to the skill directory, e.g. `pet-flavor-trial-workspace/`, under `iteration-N/<eval_name>/` with `with_skill/`, `without_skill/` (or baseline), `eval_metadata.json`, and after grading: `grading.json`, `timing.json`. Use `scripts.aggregate_benchmark` and `eval-viewer/generate_review.py` from the skill-creator skill to produce `benchmark.json` and the review viewer.
