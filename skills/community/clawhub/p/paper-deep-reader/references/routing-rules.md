# Routing Rules

This file defines how the agent should route a paper before drafting the final note.

Routing happens after an initial framing read and before the main analysis is written.

The purpose of routing is not taxonomy for its own sake. The purpose is to decide what the note must preserve, what the note must audit, and what the note must not overemphasize.

## 1. Routing principles

1. Route by intellectual load, not by title words.
2. Use the base note template by default.
3. Let routing expand or tighten sections rather than replacing the common structure.
4. Choose the simplest faithful route.
5. Do not add a second adapter just because a paper contains more than one ingredient.

## 2. Routing prerequisites

Do not route a paper before you can write a compact paper map.

At minimum, the reader should be able to write:

> The paper studies __ in the setting __. Its main move is __. It claims __, supported mainly by __. The key technical objects are __. The real intellectual load sits in __.

If this statement is still vague, keep reading before routing.

## 3. Mandatory route record

Before drafting the note, create an internal route record in this form:

```markdown
Primary adapter:
Secondary adapter:
Evidence packs:
Domain overlay:
Route confidence:
Why this route:
```

`Why this route` should explain in three to five sentences:

- what the main move is
- what kind of object must be reconstructed most faithfully
- what kind of evidence carries the main claims
- which tempting alternative routes were rejected and why

## 4. Routing order

### Step 1. Build the paper map

Identify:

- research question
- problem setting or regime
- main move
- main claims
- key technical objects
- where the paper's real load sits

### Step 2. Choose exactly one primary adapter

Choose the primary adapter that would produce the least distorted note if it were the only adapter allowed.

Questions to ask:

- What is the core contribution type?
- What must be reconstructed most faithfully for the note to remain useful later?
- Where would a smart reader most likely be misled if the wrong adapter were chosen?

### Step 3. Add a secondary adapter only if necessary

Add a secondary adapter only when:

1. the second contribution is independently central
2. it changes the note's structure in a substantial way
3. omitting it would hide a real part of the paper's contribution rather than merely condensing it

If those are not all true, do not add one.

### Step 4. Choose one to three evidence packs

Choose the evidence packs that are most likely to change the final verdict if the evidence turns out to be weak.

Do not choose packs only because they sound relevant in the abstract.

### Step 5. Add zero or one domain overlay

Use an overlay only when the domain has recurring objects, overclaims, or evaluation traps that deserve active reminders.

Do not force an overlay into every route.

### Step 6. Expand the base note template

Routing changes emphasis. It does not erase the common contract.

Always preserve the shared note structure unless the user explicitly asks for a different output format.

## 5. Tie-break rules for common mixed papers

### Method versus benchmark

Use `method-algorithm` when the paper's main value is a new mechanism and evaluation mainly supports that mechanism.

Use `benchmark-evaluation` when the paper's main value is the evaluation framework itself and methods are present mainly as test subjects.

### Method versus systems

Use `method-algorithm` when the central contribution is an algorithmic idea and systems details mainly enable implementation.

Use `system-design` when the central contribution is the deployment or infrastructure tradeoff and the algorithmic piece is supportive.

### Theory versus method

Use `theory-proof` or `optimization-convergence` when the main selling point is the formal guarantee.

Use `method-algorithm` when the theorem is informative but the real contribution remains the method itself.

### Statistical inference versus theory-proof

Use `statistical-inference` when the note must revolve around estimand, identification, estimation, and uncertainty.

Use `theory-proof` when the note must revolve around theorem structure, proof architecture, and scope of a formal claim.

### Dataset versus benchmark

Use `dataset-resource` when data collection, annotation, or release is the real contribution.

Use `benchmark-evaluation` when the distinctive contribution is the evaluation protocol, task construction, or metric design.

### Survey versus anything else

Use `survey-synthesis` when the paper's value comes primarily from taxonomy, synthesis, or conceptual organization rather than a single new result.

## 6. Route examples

### Example A: new LLM benchmark

```markdown
Primary adapter: benchmark-evaluation
Secondary adapter:
Evidence packs:
  - benchmark-fairness-and-contamination
  - robustness-and-ood
  - data-quality-labeling-leakage
Domain overlay:
  - llm-agents
```

Reason: the paper's main move is to redefine evaluation, not to introduce a new method.

### Example B: new RAG method

```markdown
Primary adapter: method-algorithm
Secondary adapter:
Evidence packs:
  - experimental-eval
  - ablation-and-mechanism-isolation
  - reproducibility-and-compute
Domain overlay:
  - retrieval-rag-memory
```

Reason: the method is the contribution; the evaluation is support.

### Example C: optimizer with convergence theorem and some experiments

```markdown
Primary adapter: optimization-convergence
Secondary adapter: method-algorithm
Evidence packs:
  - proof-rigor
  - experimental-eval
Domain overlay:
  - training-optimization-dynamics
```

Reason: the theorem is a central load-bearing contribution, but the algorithmic procedure also matters.

### Example D: LLM serving system

```markdown
Primary adapter: system-design
Secondary adapter:
Evidence packs:
  - systems-cost-latency-reliability
  - reproducibility-and-compute
  - benchmark-fairness-and-contamination
Domain overlay:
  - llm-agents
```

Reason: the paper's main value is the systems tradeoff under realistic workload assumptions.

### Example E: new curated scientific dataset

```markdown
Primary adapter: dataset-resource
Secondary adapter:
Evidence packs:
  - data-quality-labeling-leakage
  - benchmark-fairness-and-contamination
Domain overlay:
  - scientific-ml
```

Reason: data construction and resource validity are the main contribution.

## 7. Adapter-specific expansion rules

### If the primary adapter is `benchmark-evaluation`

Expand:

- `## Problem setup`
- `## Evidence`
- `## Limitations and failure modes`

Add domain blocks when useful:

- `### Task definition and metric validity`
- `### Benchmark construction and contamination risk`
- `### Slice-wise failures`

Tighten:

- `## Technical core` if there is little real mechanism beyond protocol design

### If the primary adapter is `dataset-resource`

Expand:

- `## Problem setup`
- `## Evidence`
- `## Limitations and failure modes`

Add domain blocks when useful:

- `### Data collection pipeline`
- `### Labeling protocol and quality control`
- `### Split logic, leakage, and governance`

Tighten:

- heavy theorem or algorithm subsections unless they are actually central

### If the primary adapter is `system-design`

Expand:

- workload and environment in `## Problem setup`
- control flow and bottleneck reasoning in `## Technical core`
- benchmark realism and cost accounting in `## Evidence`

### If the primary adapter is `theory-proof`

Expand:

- formal setup and theorem statements in `## Technical core`
- assumption interpretation in `## Limitations and failure modes`

Tighten:

- experimental prose when experiments are minor or absent

## 8. Evidence-pack selection heuristics

Choose evidence packs by asking:

1. What would most weaken my verdict if it turned out to be shaky?
2. What evidence type is doing the argumentative work here?
3. What failure mode is most plausible for this genre of paper?

Typical pairings:

- `method-algorithm` -> `experimental-eval`, `ablation-and-mechanism-isolation`, `reproducibility-and-compute`
- `benchmark-evaluation` -> `benchmark-fairness-and-contamination`, `robustness-and-ood`
- `dataset-resource` -> `data-quality-labeling-leakage`, often `benchmark-fairness-and-contamination`
- `system-design` -> `systems-cost-latency-reliability`, often `reproducibility-and-compute`
- `empirical-identification` -> `causal-identification`, often `data-quality-labeling-leakage`
- `theory-proof` -> `proof-rigor`

## 9. Overlay selection heuristics

Add an overlay only when the domain has specialized traps that are easy to miss during a generic read.

Examples:

- `llm-agents`: evaluator leakage, budget confounds, tool scaffolding versus planning
- `retrieval-rag-memory`: retrieval versus reasoning confounds, stale index assumptions, context budget effects
- `generative-models`: quality versus coverage tradeoffs, sampler versus objective confounds
- `quant-backtesting`: turnover, slippage, leakage, regime dependence

## 10. Self-check order after drafting

Always self-check in this order:

1. `general.md`
2. selected evidence packs
3. primary adapter-specific checks
4. secondary adapter-specific checks if used
5. overlay-specific reminders if used

The general checklist is the universal gate and should never be skipped.

## 11. Anti-patterns

Do not:

- route from title and abstract alone
- choose an adapter just because it matches the venue
- choose too many evidence packs
- add a secondary adapter to look sophisticated
- let overlays turn into replacement templates
- keep a route when later reading shows the main load lives elsewhere

## 12. Revision rule

Routing is provisional until the technical core and evidence sections have been read.

If later reading reveals that the main load sits somewhere else, update the route record and revise the note structure accordingly.
