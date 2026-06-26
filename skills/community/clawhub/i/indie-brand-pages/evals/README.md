# Evals for indie-brand-pages

Test prompts in `evals.json` follow [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) schema and are used to verify the skill produces page map, narrative structure, copy and visual guidance, and placement.

## evals.json structure (skill-creator compliant)

- **skill_name**: `indie-brand-pages` (matches SKILL.md frontmatter `name`)
- **evals**: array; each item has
  - **id**: unique integer
  - **prompt**: user task (realistic scenario)
  - **expected_output**: short description of expected result
  - **files**: input file paths relative to skill root (e.g. `evals/files/...`), or `[]`
  - **expectations**: list of verifiable statements (strings); grader uses these and writes `grading.json` with `text`, `passed`, `evidence` per expectation

## Eval coverage

1. **Eval 1** — Indie swimwear, weak About: page map (About, Our Story, Design Process), Our Story structure and sample copy.
2. **Eval 2** — Handmade bags, add Design Process and improve nav: page structure, nav placement for Story and Process.
3. **Eval 3** — Early access for repeat customers: member-only content, gated pages, loyalty platform note (e.g. Rijoy).

## Workspace and iterations

Per skill-creator: put run results in a workspace **sibling** to the skill directory, e.g. `indie-brand-pages-workspace/`, under `iteration-N/<eval_name>/` with `with_skill/`, `without_skill/` (or baseline), `eval_metadata.json`, and after grading: `grading.json`, `timing.json`. Use `scripts.aggregate_benchmark` and `eval-viewer/generate_review.py` from the skill-creator skill to produce `benchmark.json` and the review viewer.
