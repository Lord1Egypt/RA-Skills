# Module: Gate-1-Level Deep Reading

This module is self-contained. It internalizes the text-report quality bar inspired by `paper-toon-deep-reader` Gate 1, but the agent must not call or invoke `paper-toon-deep-reader` while executing `paper-code-joint-analysis`.

Use this module when writing `paper_reading_report.md`.

## Contract

`paper_reading_report.md` is the authoritative paper-only learning report. It is not a summary, dashboard copy, preface to the code analysis, or code mapping.

Do not include repository paths, source-code line numbers, class/method mappings, or code-disclosed implementation facts in `paper_reading_report.md`. Those belong in `paper_questions_for_code.md`, `paper_code_crosswalk.md`, `implementation_omissions.md`, and `experiment_joint_reading.md`.

For a normal computer-science paper, target at least 12,000 Chinese/English characters. A shorter report is acceptable only when the paper is unusually short or source material is incomplete; explain that in `validation_report.md`.

## Required Depth

Cover these sections when the source material exists:

- Paper identity, source status, title interpretation, and scope.
- The real problem, why it matters, assumptions, and failure modes of the setting.
- Related-work gap: what prior methods do, what remains unsolved, and how the paper positions itself.
- Symbols, data entities, model entities, objective variables, and notation before using formulas.
- Method components in knowledge-dependency order.
- For each complex module: input, output, dimensions when available, trainable parameters, fixed hyperparameters, data flow, and where outputs are consumed.
- Formulas, losses, and objectives as renderable math, with plain-language interpretation and derivation-level explanation when needed.
- Algorithm/control flow and at least one concrete toy walkthrough for complex methods.
- Important figures, tables, and charts: what each visual is trying to prove, how it supports the claim, and what it leaves unclear.
- Experiment design: question answered by each block, datasets, splits, baselines, metrics, ablations, result aggregation, surprising findings, and result-to-claim alignment.
- Reproducibility gaps and paper ambiguities visible from the paper alone.
- Reviewer/defense lens: novelty, significance, technical soundness, methodological rigor, missing controls, limitation honesty, and likely reviewer concerns.
- Strengths, weaknesses, structural limitations, and future directions.
- A simple teaching story that explains the paper without equations.

## Explanation Pattern

For every central idea, formula, or module:

1. Intuition.
2. Mathematical expression or algorithm step.
3. Concrete example or toy walkthrough.
4. Limitation or assumption.
5. Open question created by the paper.

The final item must feed `paper_questions_for_code.md`, where code evidence may answer it later.

## Evidence Discipline

Label evidence categories explicitly:

- `paper-stated`
- `reasonable inference`
- `not reported`

Do not use code as evidence until after the question ledger has been written.

## Non-Goals

Do not import or run cartoon-image generation, storyboard gates, visual style handshakes, or PDF assembly. Those belong to a different skill workflow.
