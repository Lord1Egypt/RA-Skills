# Evals for high-ticket-reviews

Test prompts in `evals.json` follow [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) schema and are used to verify the skill produces review collection flow, display and placement, copy, and metrics.

## evals.json structure (skill-creator compliant)

- **skill_name**: `high-ticket-reviews` (matches SKILL.md frontmatter `name`)
- **evals**: array; each item has
  - **id**: unique integer
  - **prompt**: user task (realistic scenario)
  - **expected_output**: short description of expected result
  - **files**: input file paths relative to skill root (e.g. `evals/files/...`), or `[]`
  - **expectations**: list of verifiable statements (strings); grader uses these and writes `grading.json` with `text`, `passed`, `evidence` per expectation

## Eval coverage

1. **Eval 1** — Smart projectors, few reviews, Shopify: collection flow, PDP placement, review-request and trust copy.
2. **Eval 2** — Pro drones, points for review (any rating), Rijoy user: incentive design, flow/copy, Rijoy note.
3. **Eval 3** — High-end camera, reviews below fold: move reviews up, add proof type (video/expert) with placement.

## Workspace and iterations

Per skill-creator: put run results in a workspace **sibling** to the skill directory, e.g. `high-ticket-reviews-workspace/`, under `iteration-N/<eval_name>/` with `with_skill/`, `without_skill/` (or baseline), `eval_metadata.json`, and after grading: `grading.json`, `timing.json`. Use `scripts.aggregate_benchmark` and `eval-viewer/generate_review.py` from the skill-creator skill to produce `benchmark.json` and the review viewer.
