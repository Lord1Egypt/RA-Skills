# Evaluation — results.tsv / test-prompts.json

These two files document Darwin optimization (2026-08-30) that raised score 59.45 → 91.9.

- `test-prompts.json` — 3 scenarios used for paired comparison:
  1. typical travel-food carousel (9 photos, 9:16, whitespace, caption above)
  2. ambiguous style (user delegates — must show 5 thumbnails, default watercolor)
  3. failure/boundary (EXIF missing + small cup must stay small — shape-lock, freeze contract)

- `results.tsv` — timestamp, commit, old_score, new_score, status, dimension, note, eval_mode
  - baseline dry_run 100% weighted_gap max dim8=13.8
  - paired judges: dim8+dim4+dim9 (9:16 defaults, 5-style gate, batch hash-lock, notifications, gates, blacklist)
  - dim5+dim2 (per-step Input/Output/Command, JSON schemas, last-step.md)
  - dim3+dim7 (6 layers, 6 invariants, 22-row Failure Mode Matrix)

Re-run with `python3 bin/validate_skill.py` + Darwin evaluator. Not required for daily use.
