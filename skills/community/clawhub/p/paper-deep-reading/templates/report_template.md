# Deep Reading Report: <paper-title>

Use this template together with `traceability_manifest.json`, `research_lens.json`, and `direction_board.json`.
Write the final report in Chinese when the user's current request is primarily in Chinese; keep proper nouns, fixed technical identifiers, claim IDs, filenames, and JSON keys in English. Otherwise write the report in English.

For every numbered section below:

- start with `### Anchored Points`
- add one or more claims in the exact form `- [C<section>.<index>][label] claim text`
- allowed labels are `evidence-backed interpretation`, `plausible inference`, and `speculation`
- keep the claim bullets concise and judgment-focused
- make sure every main-body claim ID appears in `traceability_manifest.json`
- if a claim is reconstructive rather than directly stated, mark it as inferential in the manifest
- if one claim depends on multiple source locations, list every materially necessary source location as separate evidence rows in `traceability_manifest.json`
- if one bullet contains multiple independent claims, split it into multiple claim IDs before writing the manifest
- after the anchored points, add the longer explanation, tables, formulas, critique, and author-side reconstruction as needed
- do not paste detailed locator bullets in the middle of the body; reserve that for the final appendix

## 1. Paper Identification and Source Package Used
### Anchored Points
After anchored points, state the title, authors, venue or status, reading mode (`LaTeX-primary`, `PDF-primary`, or mixed), exact source files used, what was searched for, what was missing, and how source limitations affect confidence.

## 2. One-Sentence Thesis and Research Equation
### Anchored Points
After anchored points, summarize the paper in one sentence and express the research equation in the form: old success -> broken assumption -> hard setting -> borrowed tool -> unavailable mechanism -> surrogate mechanism. Also include the compact form `A(P) ∩ ¬C ∩ T ∩ M => Z≈Y` when applicable.

## 3. Title Interpretation
### Anchored Points
After anchored points, interpret the title term by term and explain how each keyword maps to the actual method, setting, and claim scope.

## 4. What Problem the Paper Really Solves
### Anchored Points
After anchored points, explain the direct problem, the practical pain point, the scientific question, and the larger pressure from the parent field.

## 5. Scientific Problem Ladder
### Anchored Points
After anchored points, build the ladder explicitly from paper-local problem to broader AI or systems boundary, and note any upper-level bottlenecks introduced by the method itself.

## 6. How the Authors May Have Found This Direction
### Anchored Points
After anchored points, reconstruct the likely dissatisfaction, near-transfer from neighboring methods, blocking constraint, and why the surrogate mechanism was worth trying. Keep uncertainty explicit.

Recommended table:

| Valuable field | Painful assumption | Borrowed/emerging tool | Blocking constraint | Conceptual replacement |
|---|---|---|---|---|

## 7. How the Authors Built the Story
### Anchored Points
After anchored points, map challenge -> failure mode -> design principle -> module -> ablation or evidence, and judge whether the story forms a coherent loop instead of a bag of modules.

Recommended table:

| Challenge | Failure mode | Design principle | Module | Evidence / claim IDs |
|---|---|---|---|---|

## 8. Related Work, Key Citations, and What Was Still Missing
### Anchored Points
After anchored points, explain what the key cited works solved, what they left open, and the narrative role of each citation cluster: field anchor, limitation evidence, method ancestor, baseline pressure, protocol justification, neighboring inspiration, or contrast boundary. Add successor-paper context when it was searched.

## 9. Main Idea
### Anchored Points
After anchored points, explain the conceptual replacement or coordination logic that makes the method coherent, rather than repeating only module names.

## 10. Symbols, Assumptions, and Notation
### Anchored Points
After anchored points, introduce the important symbols, operators, assumptions, and task-specific objects before relying on them heavily later. Mark hidden assumptions that may become direction seeds.

## 11. Key Formulas and Equation-by-Equation Explanation
### Anchored Points
After anchored points, preserve the central formulas in readable math form. For each one, explain symbols, role, why this form was chosen, how it connects to adjacent modules, and what looks fragile, heuristic, under-justified, statistically weak, or expensive. Add direction triggers when modifying the formula could create a new mechanism.

## 12. Theory / Proof / Practice Mapping
### Anchored Points
After anchored points, explain what is proved, why it is proved, what reviewer concern it addresses, how theory maps to implementation, and where theory and practice diverge. For proofs, identify assumptions and ask how the proof breaks if each assumption is dropped.

## 13. Algorithm or Module Walkthrough with Concrete Example
### Anchored Points
After anchored points, give a step-by-step pipeline walkthrough with at least one concrete mini-example that instantiates inputs, intermediate states, and outputs. Use tiny examples or special cases to reveal the core idea or fragility.

## 14. Method Deep Reading: The Author-Thinking Behind Each Module
### Anchored Points
After anchored points, explain for each major module: the failure being fixed, the ideal but unavailable solution, the proxy signal actually used, the hidden assumption, the risk, and the future idea that appears if the assumption breaks.

Recommended table:

| Module | Failure fixed | Ideal unavailable solution | Available proxy | Hidden assumption | Risk under violation | Future research point |
|---|---|---|---|---|---|---|

## 15. Figure Explanation
### Anchored Points
After anchored points, interpret the key figures or captions, explain what each figure is meant to demonstrate, and judge whether the visual evidence really supports the associated claim. When figures are unavailable, state that limitation.

## 16. Experimental Design
### Anchored Points
After anchored points, explain datasets, tasks, baselines, metrics, ablations, implementation details, and how the compared methods map back to the related-work landscape. Note missing controls and statistical uncertainty.

## 17. Experiments as Story Evidence and Claim Alignment Audit
### Anchored Points
After anchored points, explain what claim each main result is supposed to support, what alternative explanation it rules out, and whether the evidence strongly, partially, or weakly supports the claim.

Recommended table:

| Experiment | Claim | Counterfactual ruled out | Metric | Stress condition | Alignment judgment |
|---|---|---|---|---|---|

## 18. Reviewer-Lens Audit
### Anchored Points
After anchored points, assess novelty, significance, soundness, methodology rigor, statistical validity, reproducibility, clarity, missing controls, limitations honesty, and any OpenReview reviewer or rebuttal signal when available. Convert the strongest reviewer-grade objections into candidate direction seeds.

## 19. Innovation Points and Claim-by-Claim Support Audit
### Anchored Points
After anchored points, list the paper's main contribution claims and judge whether each one is supported by theory, experiments, qualitative evidence, reviewer discussion, or only weak evidence.

## 20. Story-Making Pattern Worth Learning
### Anchored Points
After anchored points, extract the reusable pattern from the paper, such as a replacement story, three-module story, closed loop, two-axis empty cell, negative-result reframing, or hidden-assumption break.

## 21. Weaknesses and Limitations
### Anchored Points
After anchored points, discuss unresolved weaknesses, failure modes, scope limits, hidden costs, and where the current idea is likely to break. Distinguish engineering limitations from structural scientific limitations.

## 22. Innovation Type and Scientific-Boundary Judgment
### Anchored Points
After anchored points, judge whether the work is incremental, cross-pollinated, conceptually reframing, negative-result informative, or potentially boundary-pushing, and explain why.

## 23. Future Directions, Direction Board, and Stronger Idea Paths
### Anchored Points
After anchored points, propose next-step ideas, stronger boundary directions, alternative modules, negative-result opportunities, or more decisive experiments. Tie the best future ideas to hidden assumptions whose failure would break the current method.

Create a compact direction board in the report and mirror the full version in `direction_board.json`.

Recommended table:

| Seed ID | Seed type | Hidden assumption / gap | Research question | Minimum viable experiment | Killer objection | Killer result | Overall score |
|---|---|---|---|---|---|---|---|

For each top seed, include:

- why this direction is grounded in the current paper
- what evidence or claim ID triggered it
- what a negative result would teach
- what a first-week plan would look like

## 24. Vivid Plain-Language Story Summary
### Anchored Points
After anchored points, write a short memorable story that stays technically faithful while remaining accessible to a non-specialist.

## 25. Exact Sources Used
### Anchored Points
After anchored points, list exactly which PDFs, LaTeX files, supplementary materials, OpenReview pages, successor papers, code notes, screenshots, or other sources were used, and explicitly mention missing or ambiguous sources.

---

## Optional Structured Notes for `research_lens.json`

### Research Equation
- old success / paradigm:
- broken assumption:
- hard setting:
- borrowed tool:
- ideal unavailable mechanism:
- surrogate mechanism:

### Three-Pass Direction Mining Notes
- Pass 1 five-C triage:
- Pass 2 evidence / method / figure chain:
- Pass 3 virtual reimplementation and hidden-assumption attack:

### Challenge-to-Module Map

| Challenge | Failure mode | Design principle | Module | Evidence |
|---|---|---|---|---|

### Module Lens Table

| Module | Failure fixed | Ideal unavailable solution | Available proxy | Hidden assumption | Risk | Future research point |
|---|---|---|---|---|---|---|

### Citation Function Table

| Citation cluster | Narrative function | Assumption inherited | How the paper modifies it |
|---|---|---|---|

### Experiments-As-Story-Evidence Table

| Experiment | Claim | Counterfactual | Metric | Stress condition | Alignment judgment |
|---|---|---|---|---|---|

### Reviewer-Lens Audit
- novelty:
- significance:
- soundness:
- methodology rigor:
- statistical validity:
- reproducibility:
- limitation honesty:
- actionable reviewer objections:

### Story Pattern Worth Reusing
- pattern name:
- compact formula:
- lesson:

### Boundary-Pushing Idea List
- hidden assumption:
- what breaks:
- next mechanism worth exploring:
- minimum viable experiment:
- negative result interpretation:
- killer objection:
- killer result:
- linked claim ids:

---

## Optional Structured Notes for `direction_board.json`

For each direction seed:

- seed_id:
- title:
- seed_type:
- trigger_interpretation_type:
- paper_anchor_claim_ids:
- trigger_evidence_summary:
- hidden_assumption_or_gap:
- research_question:
- hypothesis:
- proposed_mechanism:
- minimum_viable_experiment:
- negative_result_interpretation:
- killer_objection:
- killer_result:
- first_week_plan:
- score:
- risk_level:
- expected_value:
- confidence:

---

# Appendix: Claim -> Evidence Index

Render this appendix only after the main body is complete.
Use `scripts/render_inline_trace_report.py` to append or refresh the detailed evidence appendix.

For each claim ID from the main report body, create a subsection like:

## C<section>.<index>
- Interpretation type:
- Statement:
- Research role:
- Confidence:

### Evidence 1
- Source file:
- Section path:
- Lines:
- Page:
- Locator method:
- Quote:
- Excerpt window:
- Notes:
