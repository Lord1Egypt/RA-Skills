# Initial Corpus Manifest Summary

This package records a summary manifest instead of bundling the full local PDF corpus.

## Manifest Source

- Source corpus root used during generation: `research-paper-diagram-generation-corpus/`
- Retrieval manifest source: `research-paper-diagram-generation-corpus/metadata/retrieval_manifest.json`
- Evidence map source: `research-paper-diagram-generation-corpus/extracted/evidence_map.json`
- Label summary source: `research-paper-diagram-generation-corpus/extracted/label_summary.csv`

## Counts

- Total local PDF records: 7,631.
- Verified official oral PDFs: 3,356.
- Supplemental local PDFs: 4,275.
- Processed PDFs: 7,631.
- Skipped PDFs: 0.
- Figure captions: 146,071.
- Diagram-relevant captions: 119,534.
- Multi-label figure records: 93,088.

## Use In This Skill

The skill does not need the full corpus to run on a user's target paper. It uses the corpus-derived taxonomy, pattern library, prompt rules, and review rubric embedded in this package. If the user asks to audit evidence provenance, cite this manifest summary and `references/source-corpus-notes.md`.
