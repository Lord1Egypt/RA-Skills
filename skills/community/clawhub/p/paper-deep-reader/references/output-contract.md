# Output Contract

This file defines what the final reading note must contain, how it should be structured, and how the agent should adapt it under the new routing model.

The goal is not to force every note into the same rigid shape. The goal is to ensure that every saved note is:

- technically faithful
- evidence-based
- durable enough to reuse later
- compatible with Obsidian-style markdown workflows
- explicitly routed by contribution type and evidence risk

## 1. Default output format

Unless the user asks for something else, save the note as a single markdown file.

The note should be:

- valid markdown
- compatible with Obsidian
- headed by YAML frontmatter
- readable as a standalone research note
- detailed enough that the user can revisit it months later without reopening the paper immediately

## 2. Frontmatter contract

Use YAML frontmatter at the top of the note.

Keep it simple and Obsidian-friendly.

Required keys:

```yaml
---
id:
created:
updated:
source:
title:
authors:
year:
venue:
status:
doi:
url:
fields: []
tags:
  - reading-note
---
```

### Rules

- Preserve YAML validity.
- Use empty values rather than inventing metadata.
- Add domain tags only when grounded in the paper.
- Do not add speculative tags.
- Keep the frontmatter lightweight; detailed interpretation belongs in the body, not the metadata.

## 3. Required body sections

These sections form the base contract for most papers.

1. `# Title`
2. `## Citation`
3. `## One-paragraph summary`
4. `## Paper map`
5. `## Why this paper matters`
6. `## Problem setup`
7. `## Main idea`
8. `## Technical core`
9. `## Evidence`
10. `## Limitations and failure modes`
11. `## Relationship to other work`
12. `## Open questions`
13. `## Implementation / reproduction notes` when relevant
14. `## What I learned from this paper`
15. `## Verdict`

These section names may be lightly adapted for readability, but the intellectual content must remain present.

## 4. Mandatory intellectual content

A note is not complete unless it includes all of the following at an appropriate level of depth.

### A. Problem reconstruction

The note must state:

- what question the paper studies
- in what setting or regime
- why the question matters
- what the main contribution actually is
- what kind of contribution it is

### B. Technical spine

The note must preserve the core formal or operational structure whenever the paper depends on it.

This may include:

- notation
- governing equations
- objective functions
- estimators
- theorem statements
- proof ideas
- identification logic
- algorithms
- benchmark construction
- dataset construction and labeling logic
- state dynamics
- complexity statements
- workload or deployment tradeoffs

Do not replace this spine with pure prose when the formal or operational structure matters.

### C. Evidence traceability

The note must make clear:

- what the paper claims
- what supports each important claim
- how strong the support is
- what caveats remain
- what evidence risks are most relevant for this paper

### D. Judgment

The note must distinguish among:

- what the authors explicitly claim
- what the evidence supports
- what you infer as a careful reader

## 5. Mandatory internal structures

These may be rendered directly in the note or reflected implicitly, but they must be constructed before finalizing.

### Paper map

At minimum:

- research question
- setting
- main move
- major claims
- key technical objects
- evidence backbone
- where the paper's real load sits
- primary failure risk

### Route record

At minimum:

- primary adapter
- secondary adapter if any
- one to three evidence packs
- domain overlay if any
- route confidence
- why this route

### Notation table

Use a notation table when notation is nontrivial.

Minimum columns:

| Symbol | Meaning | Type / shape / domain | Units / scale | First appears where |
|---|---|---|---|---|

### Claim-evidence matrix

Use a claim-evidence matrix whenever the paper makes multiple important claims.

Minimum columns:

| Claim | Stated by authors or my inference? | Evidence source | Strength | Caveat |
|---|---|---|---|---|

### Limitation ledger

Separate:

- author-acknowledged limitations
- reader-inferred limitations

## 6. Routing contract

The base template is universal, but the note must adapt to the paper's routed contribution type and evidence profile.

### General routing rule

- Choose exactly one **primary adapter**.
- Add a **secondary adapter** only when a second contribution is independently central.
- Choose **one to three evidence packs** that match the main claim risks.
- Use a **domain overlay** only when it materially improves faithfulness.
- Expand or tighten sections of the base template; do not replace the common structure.

### Theory / mathematics / statistics

When routed to `theory-math-stats`, the final note should emphasize:

- definitions and setup
- theorem statements
- assumptions and which ones do real work
- proof strategy
- rates, guarantees, or consistency claims
- relation to nearby theory

The note should not waste space on experimental sections if the paper has little or none.

When `proof-rigor.md` is one of the evidence packs, the note should be especially disciplined about separating exact formal claims from practical interpretations.

### Method / algorithm

When routed to `method-algorithm`, the final note should emphasize:

- model or estimator definition
- objective and update rule
- architecture or operator choices that materially matter
- optimization or training details
- the component claimed to drive the gain
- reproducibility-sensitive implementation details

When relevant, the note should also reflect the chosen evidence packs, such as:

- `experimental-eval.md` for experiment quality and baseline strength
- `ablation-and-mechanism-isolation.md` for whether the claimed mechanism is really isolated
- `robustness-and-ood.md` for generalization limits
- `benchmark-fairness-and-contamination.md` for evaluation integrity
- `reproducibility-and-compute.md` for hidden compute or engineering asymmetries

### Benchmark / evaluation

When routed to `benchmark-evaluation`, the final note should emphasize:

- what capability or property is being measured
- why earlier evaluation was inadequate
- benchmark construction and scope
- metric validity
- fairness of the compared systems
- contamination, leakage, or evaluator bias risk
- slice-wise failures and failure cases

### Dataset / resource

When routed to `dataset-resource`, the final note should emphasize:

- data collection pipeline
- sampling frame
- annotation protocol
- quality control
- split logic
- artifact risk
- licensing, governance, privacy, and intended use

### Empirical / economics / social science

When routed to `empirical-econ`, the final note should emphasize:

- estimand
- identification strategy
- data construction
- measurement choices
- robustness checks
- threats to validity
- correlation versus causality

### Survey / synthesis

When routed to `survey-synthesis`, the final note should emphasize:

- scope and selection logic
- organizing axis or taxonomy
- what distinctions are genuinely illuminating
- coverage gaps or bias
- what the synthesis changes in the reader's understanding of the area

### Replication / negative result

When routed to `replication-negative-result`, the final note should emphasize:

- target claim being tested
- fidelity of the reproduction or stress test
- mismatch between original and reproduction settings
- what fails and where
- what uncertainty remains after the negative or null result

### Physics

When routed to `physics`, the final note should emphasize:

- physical question
- regime of validity
- assumptions and approximations
- boundary conditions, symmetries, or conserved quantities when relevant
- limiting cases
- mapping from theory to observables

### Quantitative finance

When routed to `quant-finance`, the final note should emphasize:

- objective: pricing, forecasting, hedging, execution, or allocation
- stochastic setup and state variables
- no-arbitrage or martingale logic when relevant
- calibration or estimation procedure
- backtest design
- risk-adjusted metrics
- frictions such as cost, turnover, and slippage

### Systems

When routed to `systems`, the final note should emphasize:

- bottleneck
- design tradeoff
- workload and environment
- hardware or software assumptions
- benchmarking fairness
- latency, throughput, memory, reliability, or cost metrics

## 7. Section insertion rules

Use the base template by default. Insert or expand routed material only where it helps the note become more faithful.

### Insert a dedicated notation table when:

- there are many recurring symbols
- the same notation is reused across sections
- domain-specific symbols would otherwise become confusing

### Insert displayed equations when:

- the paper's mechanism depends on them
- the estimand or objective must be preserved exactly
- a theorem or law loses meaning without formal notation

### Insert pseudocode or numbered procedural steps when:

- implementation order matters
- the paper's algorithm is easier to reconstruct procedurally
- the paper omits operational detail that must be inferred carefully

### Insert additional routed sub-blocks when needed, such as:

- `### Assumptions and approximations`
- `### Identification logic`
- `### Task definition and metric validity`
- `### Benchmark fairness and contamination risk`
- `### Data collection pipeline`
- `### Labeling protocol and quality control`
- `### Failure cases and slice behavior`
- `### Evidence risks / audit notes`
- `### Physical interpretation`

## 8. Length and depth rules

Default to durable depth rather than compression.

A good note should be:

- shorter than the paper
- much more structured than the paper
- explicit about the paper's real mechanism
- selective rather than exhaustive
- clear about which evidence risks were checked

Do not pad the note. Do not compress away the crucial logic.

## 9. Style contract

The final note should be written in a style that is:

- precise
- pedagogical
- non-hyped
- reusable
- comfortable to read in plain markdown

### Use

- short paragraphs
- headings
- displayed math for important formulas
- tables when they clarify structure
- code fences for pseudocode or implementation detail

### Avoid

- vague praise
- empty novelty language
- long abstract-like paraphrases
- unsupported evaluative claims
- pretending to know what the paper does not specify

## 10. Appendix and supplement rule

A note is incomplete if a major claim depends on appendix-only material that was not read.

You must consult appendix or supplement sections when they contain:

- proof ideas needed for interpretation
- robustness checks central to the empirical claim
- ablations central to the method claim
- benchmark design or contamination checks central to the evaluation claim
- dataset construction details central to the resource claim
- missing implementation details needed for reproduction
- caveats or failure cases omitted from the main text

## 11. Saving contract

When saving is requested:

- use markdown
- preserve Obsidian-compatible frontmatter
- prefer the user-specified location if given
- otherwise save next to the paper as `detailed-note.md`

## 12. Minimum acceptance test

Do not finalize the note until all of the following are true.

- A careful reader could recover the main problem and main move from the note alone.
- The note preserves the real technical or operational spine of the paper.
- Authors' claims, evidence, and your judgment are clearly separated.
- The route record would still make sense to a careful reader after the note is written.
- At least one meaningful limitation, caveat, or missing check is stated.
- The note would still be useful as a research reference later.
