---
name: jane-street-puzzle-archivist
description: Use when solving, organizing, or reviewing Jane Street monthly puzzles, especially when bootstrapping a new puzzle month, comparing against prior public solutions, capturing reusable solving patterns, submitting answers, or updating the long-lived puzzle archive and knowledge base.
---

# Jane Street Puzzle Archivist

Use this skill to keep Jane Street puzzle work reproducible, archived, and reusable.

## When to Use

- A new monthly Jane Street puzzle is live.
- An existing month needs solver cleanup, answer submission, or better notes.
- You need to compare the current puzzle with prior public solution repos.
- You want to turn puzzle-solving experience into reusable scripts, docs, or skills.

## Workflow

1. Run `python3 scripts/current_puzzle.py` to inspect the live puzzle metadata.
2. If it is a new month, run `python3 scripts/current_puzzle.py --init` and work inside `puzzles/YYYY/YYYY-MM-slug/`.
3. Refresh the reference index with `python3 scripts/index_reference_repos.py`.
4. Read:
   - `references/reference-repos.md`
   - `references/solving-patterns.md`
5. Solve the puzzle with a reproducible script stored in the month folder.
6. Record the answer and submission status in that month's `README.md` and `submission.json`.
7. If you learned a reusable technique, update this skill or the repo knowledge files before finishing.

## Required structure

- Each puzzle lives under `puzzles/YYYY/YYYY-MM-slug/`.
- Keep the puzzle asset, solver, notes, metadata, and submission record together.
- Do not commit `refs/` or `.omx/`.

## Publishing

- This skill can be published directly with:
  - `clawhub publish .agents/skills/jane-street-puzzle-archivist --slug jane-street-puzzle-archivist --name "Jane Street Puzzle Archivist" --version <semver>`
- If the skill changes materially, publish a new version after verifying the references still match the repo workflow.
