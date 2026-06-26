# Paper Taxonomy

This file defines the vNext taxonomy for routing papers into adapters, evidence checklist packs, and domain overlays.

The goal is not to create a huge number of rigid templates. The goal is to make routing more faithful to the real shape of modern papers, especially arXiv papers that mix method, evaluation, data, theory, and systems contributions.

## 1. Design principles

1. Keep the base note template universal.
2. Separate narrative structure from evidence auditing.
3. Route by the paper's real intellectual load, not by surface buzzwords.
4. Prefer a small number of reusable primitives over many brittle domain-specific templates.
5. Let mixed papers use composition, but only when the second component is genuinely load-bearing.

## 2. Three-layer model

### Layer A: Primary adapter

The primary adapter answers:

> What kind of contribution is this paper mainly making?

This layer determines the main narrative skeleton of the note.

### Layer B: Evidence checklist packs

Evidence packs answer:

> What kind of evidence is carrying the paper's central claims?

This layer determines what should be audited, doubted, or stress-tested before the note is finalized.

### Layer C: Domain overlays

Domain overlays answer:

> What domain-specific objects, confusions, and failure patterns should the reader actively watch for?

This layer is light by design. It adds domain reminders without replacing the base structure.

## 3. Primary adapters

Choose exactly one primary adapter for every paper.

Add a secondary adapter only when a second contribution is independently central.

### `theory-proof`

Use when the main contribution is a theorem, proof technique, guarantee, approximation result, consistency claim, or formal characterization.

The note should emphasize:

- exact setup and definitions
- theorem statements
- assumptions and which ones do real work
- proof architecture
- rates, guarantees, or scope of validity
- special cases and reductions to prior theory

### `statistical-inference`

Use when the main contribution is an estimand, estimator, identification result, inference procedure, uncertainty quantification method, or asymptotic or finite-sample statistical property.

The note should emphasize:

- target quantity
- estimand versus estimator
- identification conditions
- estimation and inference pipeline
- finite-sample versus asymptotic regime
- efficiency, bias, consistency, and uncertainty quantification

### `optimization-convergence`

Use when the paper's central load sits in an objective, update rule, optimization geometry, convergence argument, stability claim, or complexity guarantee for an optimization procedure.

The note should emphasize:

- optimization problem and objective
- algorithmic step or update rule
- stationarity versus optimality
- assumptions controlling convergence
- rate or complexity notion
- practical consequences for training or tuning

### `method-algorithm`

Use when the paper proposes a model, algorithm, operator, training recipe, inference mechanism, or estimator and supports it with experiments, simulations, or empirical results.

The note should emphasize:

- exact mechanism
- the component claimed to drive the gain
- architecture or operator choices that matter
- training or optimization recipe
- baselines, ablations, and robustness
- details that would matter in reimplementation

### `empirical-identification`

Use when the main contribution is an empirical design, identification strategy, measurement strategy, or evidence-based claim from observational, experimental, or institutional data.

The note should emphasize:

- scientific or causal question
- estimand
- identification logic
- data construction
- measurement choices
- threats to validity and robustness

### `system-design`

Use when the main contribution is a systems design, infrastructure mechanism, implementation strategy, performance engineering idea, or deployment tradeoff under a concrete workload and environment.

The note should emphasize:

- bottleneck
- design idea
- workload and deployment setting
- hardware and software assumptions
- benchmark realism and fairness
- latency, throughput, memory, reliability, energy, or cost tradeoffs

### `benchmark-evaluation`

Use when the main contribution is a benchmark, evaluation protocol, task operationalization, judge or evaluator design, or a new framework for comparing systems or models.

The note should emphasize:

- what is being measured
- why earlier evaluation was inadequate
- benchmark construction and scope
- metric validity
- baseline fairness
- contamination, leakage, or gaming risk
- slice-wise behavior and failure cases

### `dataset-resource`

Use when the main contribution is a dataset, labeling protocol, curated corpus, released resource, or data construction pipeline.

The note should emphasize:

- collection pipeline
- sampling frame
- annotation protocol
- quality control
- split logic
- artifact risk
- licensing, governance, privacy, and intended use

### `survey-synthesis`

Use when the main contribution is a taxonomy, synthesis, conceptual reorganization, trend map, or broad review of a field rather than a single new method or theorem.

The note should emphasize:

- scope and selection logic
- organizing axis or taxonomy
- what distinctions are actually illuminating
- coverage gaps or bias
- whether the synthesis changes how a reader should think about the area

### `replication-negative-result`

Use when the main contribution is a replication attempt, failed reproduction, null result, stress test of a prior claim, or a careful demonstration that a popular result is narrower than advertised.

The note should emphasize:

- target claim being tested
- fidelity of the replication
- mismatch between original and reproduction settings
- where the original claim breaks
- what uncertainty remains after the negative result

## 4. Evidence checklist packs

Use the general checklist first for every paper.

Then choose one to three evidence packs that match the main claim risks.

### `proof-rigor`

Audit:

- theorem fidelity
- assumption structure
- proof strategy
- boundary of the formal claim
- asymptotic versus practical interpretation

### `experimental-eval`

Audit:

- experiment design
- strength and fairness of baselines
- whether the results answer the paper's actual claim
- whether evidence is broad or narrow

### `benchmark-fairness-and-contamination`

Audit:

- task and metric fairness
- train-test leakage or contamination
- evaluator or judge bias
- hidden tuning or budget asymmetry
- whether the benchmark rewards the claimed capability

### `ablation-and-mechanism-isolation`

Audit:

- whether the claimed mechanism is isolated cleanly
- whether the strongest ablation is present
- whether gains could instead come from scale, engineering, or tuning

### `robustness-and-ood`

Audit:

- shift robustness
- long-tail behavior
- adversarial or noisy settings
- whether evidence is IID-only

### `data-quality-labeling-leakage`

Audit:

- sampling and collection
- labeling quality
- split leakage
- shortcut artifacts
- governance and resource validity

### `reproducibility-and-compute`

Audit:

- training budget
- hardware dependence
- data and hyperparameter asymmetries
- implementation-sensitive details
- whether the method gain is actually a compute gain

### `systems-cost-latency-reliability`

Audit:

- latency, throughput, memory, reliability, energy, and cost accounting
- benchmark realism
- sensitivity to hardware, workload, scale, and deployment assumptions

### `causal-identification`

Audit:

- estimand definition
- identification assumptions
- measurement validity
- robustness and sensitivity
- external validity

### `synthesis-scope-and-coverage`

Audit:

- scope
- inclusion and exclusion logic
- selection bias
- taxonomy quality
- conceptual sharpness

## 5. Domain overlays

Domain overlays are intentionally lightweight.

They should be used only when the field has recurrent technical objects, overclaims, or failure modes that deserve special reminders.

Recommended early overlays:

- `llm-agents`
- `retrieval-rag-memory`
- `generative-models`
- `multimodal`
- `training-optimization-dynamics`
- `mechanistic-interpretability`
- `causal-ml-econometrics`
- `scientific-ml`
- `physics-informed`
- `quant-backtesting`

Each overlay should contain only:

1. common technical objects
2. common overclaims or confusions
3. extra evidence to inspect
4. optional note prompts

## 6. Composition rules

### Default rule

Use:

- one primary adapter
- one to three evidence packs
- zero or one domain overlay

### Secondary adapter rule

Add a secondary adapter only when both of the following are true:

1. the second contribution is independently central rather than supportive
2. omitting it would materially distort the final note

### Examples

- New method plus experiments: `method-algorithm`
- New benchmark used to compare existing methods: `benchmark-evaluation`
- New optimizer whose main value is the convergence theorem: `optimization-convergence`
- New serving stack for LLM inference: `system-design`
- New dataset with annotation protocol and benchmark tasks: `dataset-resource`

## 7. Migration map from the current structure

### Current files that stay conceptually central

- `checklists/general.md`
- `references/note-template-base.md`
- `references/output-contract.md`

### Current files that should be renamed or split

- `adapters/ml-method.md` -> `adapters/method-algorithm.md`
- `checklists/ml.md` -> split into:
  - `experimental-eval.md`
  - `ablation-and-mechanism-isolation.md`
  - `reproducibility-and-compute.md`
- `adapters/theory-math-stats.md` -> split into:
  - `theory-proof.md`
  - `statistical-inference.md`
  - `optimization-convergence.md`
- `checklists/theory-math-stats.md` -> split at least into:
  - `proof-rigor.md`
  - later optional inference- and optimization-specific audit files
- `adapters/systems.md` -> `adapters/system-design.md`
- `checklists/systems.md` -> `checklists/systems-cost-latency-reliability.md`

### New files with highest immediate payoff

- `adapters/benchmark-evaluation.md`
- `adapters/dataset-resource.md`
- `checklists/benchmark-fairness-and-contamination.md`
- `checklists/reproducibility-and-compute.md`

## 8. File schemas

### Adapter schema

Every adapter should use the same skeleton:

```markdown
# Adapter: <name>

## Use when
## What to prioritize
## Questions to answer in the note
## Minimum insertions into the note
## Special reading rules
## Typical failure patterns to watch for
## Reusable note prompts
```

### Checklist schema

Every checklist should use the same skeleton:

```markdown
# Checklist: <name>

Run this after the general checklist.

## <theme>
- [ ] ...

## Skepticism / failure risks
- [ ] ...

## If the answer is weak, reflect it in the note
- [ ] I changed the claim-evidence matrix accordingly.
- [ ] I recorded at least one caveat in Limitations and failure modes.
- [ ] I weakened my verdict if the support is narrow.
```

### Overlay schema

Every overlay should use the same lightweight skeleton:

```markdown
# Overlay: <name>

## Common technical objects
## Common overclaims or confusions
## Extra evidence to inspect
## Domain-specific note prompts
```

## 9. Acceptance standard for the taxonomy

The taxonomy is working if it makes the final note more faithful along all three axes:

1. the technical core is reconstructed more accurately
2. the evidence is audited more sharply
3. mixed papers are handled without bloating the note

If a new taxonomy branch does not improve at least one of those, do not add it.
