# Builder-Time Acquisition Report

## Source

The user already had the papers downloaded in the project. No new paper download was required for this generated skill.

The builder used:

- `paper_index/README.md`
- `paper_index/papers.jsonl`
- `paper_index/file_assets.jsonl`
- `research-paper-diagram-generation-corpus/metadata/retrieval_manifest.json`
- `research-paper-diagram-generation-corpus/extracted/extraction_summary.json`
- `research-paper-diagram-generation-corpus/extracted/figure_inventory.csv`
- `research-paper-diagram-generation-corpus/extracted/label_summary.csv`

## Acquisition Status

- Existing local PDFs indexed: 7,631.
- Accessible PDFs processed in existing extraction artifacts: 7,631.
- Skipped PDFs: 0.
- New downloads during this skill generation: 0.
- Access basis: user-provided local project corpus plus previously indexed public/open materials.

## Focus Subset Construction

The inspiration/case focus subset was constructed from existing extracted captions and labels. It used multi-label figure categories such as `case_walkthrough`, `failure_limitation`, `mechanism_intuition`, `evidence_board`, `taxonomy_design_space`, and `data_benchmark_protocol`, plus broad motivation keywords.

This is sufficient for a reusable figure-production skill because the output is a taxonomy, workflow, prompt policy, and review rubric rather than a claim about a single paper's empirical result.

## Reliability Boundary

The acquisition and extraction artifacts are full-feasible over local PDFs, but the inspiration/case subset is automated and broad. For final publication figures, the generated skill must still ground every case, metric, label, and example in the user's target paper material.
