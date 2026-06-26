# Evidence Lineage Summary

The full local evidence map supports these skill claims:

1. Inspiration figures are not one visual genre; they combine case walkthroughs, failure/limitation maps, mechanism intuitions, evidence boards, design-space hooks, and scenario storyboards.
2. The core reader question is "why is this paper needed?", which differs from method-framework figures that primarily answer "what is the method?"
3. The same figure can be multi-label: one case may show a failure, an observation, a mechanism intuition, and the need for a proposed method.
4. Case evidence must remain faithful to the target paper. Inspiration figures are especially prone to overclaiming because they compress a paper's motivation into one memorable story.
5. Layout choice should follow the inspiration source: case -> storyboard, failure -> failure chain, contrast -> split screen, observation -> ladder, taxonomy -> map, evidence -> tile board.
6. When multiple schemes are plausible, the skill should move toward generated candidate images or schematic candidates, usually 6, instead of asking the user to compare only text.

These claims are backed by `research-paper-diagram-generation-corpus/extracted/evidence_map.json`, `figure_inventory.csv`, and `label_summary.csv`.

## Full-Corpus Counts

- Processed local PDF records: 7,631.
- Verified official oral PDFs: 3,356.
- Supplemental local PDFs: 4,275.
- Extracted figure captions: 146,071.
- Diagram-relevant captions: 119,534.
- Multi-label diagram records: 93,088.
- Representative rendered pages: 96.

## Inspiration/Case Focus Counts

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

## Example Evidence Signals

- First-figure visual summaries often serve as an inspiration hook.
- Failure-mode figures often motivate an algorithmic, evaluation, or safety contribution.
- Case walkthroughs often make abstract model behavior inspectable.
- Evidence boards often turn a qualitative concern into a paper-level claim.
- Design-space maps often reveal a missing region that motivates the proposed method.
