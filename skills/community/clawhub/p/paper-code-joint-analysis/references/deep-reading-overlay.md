# Deep Reading Overlay

This overlay adapts the text-analysis strengths of a Gate-1-level paper deep-reading report for paper-code joint analysis.

Do not call or import `paper-toon-deep-reader` at runtime. Do not import cartoon-image, storyboard, or final-PDF gates into this skill. This skill's deliverable is a paper-only deep-reading report plus code-grounded companion artifacts and a reusable static reader. The useful part to preserve is the rigorous teaching/reporting method, now internalized in `modules/deep-reading-gate1.md`.

## Gate-1 Depth Requirement

`paper_reading_report.md` should match the depth expected from a Gate-1-level text deep-reading report. It is the authoritative paper-only learning report, not a short preface to the code analysis and not a source-code mapping.

For a normal computer-science paper, the report should usually be at least 12,000 Chinese/English characters. A shorter report is allowed only when the source paper is unusually short or lacks enough material; in that case, explain the reason in `validation_report.md`.

The report must explicitly cover, when source material exists:

- paper identity, title interpretation, and source status;
- what problem the paper truly solves, why it matters, and what assumptions it makes;
- what related work or prior methods did, what gap remains, and how this paper positions itself;
- symbols, entities, datasets, model objects, and notation before formulas are used;
- the proposed method in knowledge-dependency order, including module inputs/outputs, trainable parameters, fixed hyperparameters, and data flow;
- formulas and losses with typeset math, plain-language interpretation, and derivation-level explanation when needed;
- algorithm/control flow with at least one concrete toy walkthrough when the method is complex;
- important figures, tables, and charts: what each visual claims, how it supports the argument, and what it leaves unclear;
- theory/proof/objective discussion when present, including what concern the theory addresses and where it stops matching implementation;
- design-choice critique: which parts are heuristic, subjective, brittle, under-justified, expensive, or likely to fail;
- experiment design: question answered by each block, datasets, splits, baselines, metrics, ablations, result aggregation, surprising findings, and whether evidence supports the stated claim;
- reproducibility gaps and paper ambiguities visible from the paper alone;
- reviewer/defense lens: novelty, significance, technical soundness, methodological rigor, result-to-claim alignment, missing controls, limitation honesty, and likely reviewer concerns;
- strengths, weaknesses, structural limitations, and future directions;
- a simple teaching story that explains the paper without equations.

Because this skill adds code analysis, every Gate-1 section should record what remains unclear from the paper alone. Those questions must be transferred into `paper_questions_for_code.md`, where the code answers or fails to answer them.

## Report Order

Write the deep-reading report in knowledge-dependency order:

1. paper identity, source status, and analysis scope;
2. problem, assumptions, and why the problem matters;
3. symbols, entities, data objects, model objects, and notation;
4. method components and their input/output;
5. formulas, losses, and objectives;
6. algorithm/control flow;
7. paper-only ambiguities, underspecified algorithm details, and reproducibility questions;
8. experiments, baselines, ablations, and supplementary studies;
9. reproducibility gaps, limitations, and modification guidance.

## Question-Led Code Reading

After the first PDF pass and before treating code as an answer, create `paper_questions_for_code.md`.

Ask explicitly:

- What does the PDF not define, not parameterize, or not operationalize?
- Which formulas have undefined symbols, unclear dimensions, unclear normalization, or unclear loss weighting?
- Which model/data-flow steps are underspecified, such as what is stored, exchanged, reused, sampled, or aggregated?
- Which experiment settings are not enough to reproduce commands, ablations, metrics, seeds, splits, or result aggregation?
- Do any paper sections, figures, tables, algorithms, or appendix statements appear inconsistent?

Then read the code to answer those questions. Mark each answer as code-confirmed, partly answered, contradiction, reasonable inference, or not reported.

## Explanation Pattern

For every central concept, module, or formula, explain:

- intuition;
- mathematical expression or algorithm step;
- concrete example or toy walkthrough when useful;
- limitation, assumption, or failure mode;
- paper-only open question or unclear implementation requirement.

## Evidence Labels

Separate these categories explicitly:

- paper-stated;
- reasonable inference;
- not reported.

Do not include code-confirmed or code-differs evidence in `paper_reading_report.md`; those belong in companion artifacts after repository reading.

## Module Detail

For every complex module, include when available:

- input and output;
- symbols and dimensions;
- trainable parameters;
- fixed hyperparameters;
- data flow;
- where the output is consumed;
- open questions about what implementation would need to decide.

## Figures, Tables, And Experiments

Important figures and tables must be interpreted, not merely listed.

For each experiment block, state:

- what question it answers;
- which paper claim it supports;
- datasets, splits, metrics, baselines, and ablations;
- whether the paper itself reports baseline implementation sources clearly;
- what the paper does not disclose and therefore needs code inspection later;
- whether the evidence really supports the stated claim.

## Reviewer And Teaching Lens

Include a concise reviewer/defense lens:

- novelty;
- significance;
- technical soundness;
- methodological rigor;
- reproducibility;
- result-to-claim alignment;
- missing baselines or controls;
- limitation honesty.

End the report with a short teaching story or summary that explains the paper without equations.
