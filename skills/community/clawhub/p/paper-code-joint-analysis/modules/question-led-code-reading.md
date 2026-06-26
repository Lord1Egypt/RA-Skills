# Module: Question-Led Code Reading

Use this module after the first paper pass and before treating code as an answer.

The input to this module is the PDF plus the completed `paper_reading_report.md`. Questions should be the reader's doubts after a serious deep read: unclear algorithm/model details, underspecified formulas, ambiguous training/inference flow, unclear experiment descriptions, missing reproducibility details, and possible inconsistencies.

## Required Artifacts

Produce both:

- `paper_questions_for_code.md`: human-readable question ledger raised by the paper deep read, then answered or flagged with code evidence.
- `analysis_bundle.json.paper_questions`: machine-readable rows for the reader template.

## Question Categories

Ask what the PDF leaves unclear in these categories:

- Missing implementation details: defaults, hidden flags, seeds, optimizer, scheduler, sample counts, thresholds, augmentations, hardware/runtime assumptions.
- Formula or objective ambiguity: undefined symbols, dimensions, normalization, loss weighting, train/inference differences.
- Model or algorithm flow ambiguity: what enters each module, what is stored, exchanged, reused, sampled, generated, validated, or aggregated.
- Experiment ambiguity: commands, dataset ratios, splits, baselines, ablation switches, metrics, standard deviation source, result aggregation.
- Apparent inconsistency: paper text, formulas, figures, tables, algorithms, appendix, and code disagree or require inference.

## Status Labels

Use exactly these statuses in `analysis_bundle.json.paper_questions`:

- `answered_by_code`
- `partly_answered_by_code`
- `not_answered`
- `contradiction`
- `reasonable_inference`

## Evidence Rules

- Keep paper evidence and code evidence separate.
- Use real file paths, class names, method names, argument names, and line ranges.
- Carry unresolved or partly answered questions into `implementation_omissions.md` and `validation_report.md`.
