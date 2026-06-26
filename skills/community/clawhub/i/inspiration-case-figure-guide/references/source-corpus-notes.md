# Source Corpus Notes

This skill was generated from the project-local full-feasible diagram corpus used by `research-paper-figure-skill-factory` v1.0.1.

The underlying extraction artifacts are summarized in this package rather than bundled as thousands of PDFs. The builder run used the project-local corpus rooted at `research-paper-diagram-generation-corpus/`.

## Coverage Summary

- Corpus processing scope: `all_accessible_relevant_pdfs`.
- Candidate PDF count: 7,631.
- Accessible PDF count: 7,631.
- Processed PDF count: 7,631.
- Skipped PDF count: 0.
- Skipped reasons: none recorded.
- Verified official oral PDFs: 3,356.
- Supplemental local PDFs: 4,275.
- Figure captions extracted: 146,071.
- Diagram-relevant captions: 119,534.
- Multi-label figure records: 93,088.
- Representative rendered pages: 96, audit aids only.

## Inspiration/Case Evidence Subset

The inspiration/case subset was derived by combining the local multi-label figure inventory with broad motivation keywords such as motivating, inspiration, case, example, failure, limitation, challenge, problem, scenario, illustration, intuition, qualitative, teaser, comparison, contrast, gap, observation, phenomenon, and analysis.

- Keyword-and-label matched records: 48,536.
- Matched papers: 7,021.
- Matched papers with first-figure signal: 2,958.

| Label | Matched Caption Count | Matched Paper Count |
|---|---:|---:|
| evidence_board | 30,611 | 6,215 |
| case_walkthrough | 23,288 | 5,826 |
| mechanism_intuition | 17,413 | 4,713 |
| data_benchmark_protocol | 10,385 | 3,429 |
| failure_limitation | 9,628 | 3,440 |
| taxonomy_design_space | 2,405 | 1,248 |

Counts are multi-label and can sum above the number of matched records.

## Classification Policy

Classification is multi-label. A single paper or diagram may simultaneously be a motivating case, failure map, evidence board, mechanism intuition, design-space hook, or method teaser. Do not force exclusive labels during routing. First collect all applicable labels, then choose the primary production subtype for the user's target figure.

## Sufficiency

- Evidence sufficiency level: `full_taxonomy`.
- Lock grade: `production_grade`.
- Lock basis: `full_taxonomy`.

Known limitations:

- Evidence extraction used automated PDF text/caption extraction, title/caption multi-label classification, and keyword filtering; it is not exhaustive manual annotation of every figure.
- The subset is broad because inspiration figures are expressed through many caption forms rather than one stable label.
- Supplemental local PDFs support taxonomy breadth but are not counted as verified official oral evidence.
- For very narrow domain styling, ask for sample images or refresh with closer domain papers.
