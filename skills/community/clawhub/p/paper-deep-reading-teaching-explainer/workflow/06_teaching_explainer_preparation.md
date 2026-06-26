# Step 6: Teaching-Explainer Preparation

After the full deep-read and research-generative audit, prepare the paper for explanation to another person.

## Inputs

Use only materials already inside the uploaded bundle and the authoritative detailed report draft:

- paper PDF / LaTeX / appendix
- visual manifest / generated page images if available
- OpenReview or rebuttal bundle if available
- intermediate JSON
- the current detailed report draft

Do not reopen external retrieval in this stage. If missing context would improve teaching, record it as a collection-stage gap.

## Procedure

1. Identify the target audience. If not specified, default to a graduate student outside the narrow subfield plus a skeptical reviewer/advisor.
2. Write the 30-second, 3-minute, and 10-minute explanations.
3. Extract the teaching story spine: before -> pain -> broken assumption -> key replacement -> mechanism -> evidence -> caveat -> next idea.
4. Build the prerequisite map: concepts, symbols, task setting, benchmark conventions, and assumptions.
5. Reorder the explanation by knowledge dependency: symbols -> data/input -> model/modules -> training/inference -> experiments/limitations.
6. Convert every key concept into an intuition -> formula -> concrete example -> limitation explanation.
7. Convert central formulas into a formula teaching table.
8. Convert complex modules into input/output/symbol/dimension/parameter/data-flow tables.
9. Convert key figures/tables into visual teaching scripts.
10. Convert experiments into question-answer evidence units, including dataset scale, labels, baseline source, metric meaning, result exceptions, and reproduction risk.
11. Add a missing-detail ledger for hardware, runtime, hyperparameters, baseline provenance, split protocol, seeds, and preprocessing.
12. Build one complete numeric toy example that connects training and inference.
13. Build role-play discussion prompts.
14. Build Q&A and defense bank.
15. Add misunderstanding guardrails and teachback self-test questions.
16. Merge all teaching outputs into the authoritative report.
17. If sidecars are requested or useful, generate them under `generated/teaching/<paper-slug>/` as derivatives of the authoritative report.

## Quality bar

A teaching section passes only if it helps someone explain the paper accurately without hiding:

- the core formula/mechanism;
- the evidence chain;
- the strongest caveat;
- the reviewer concern;
- the future research hook.
- the reproduction-critical details that are present and missing;
- one concrete numeric example that can be explained at the board.
