# Phase: Experiment Design

## Goal

Create a locked, reviewable experimental protocol that specifies exactly what will be
tested, how, and what constitutes success — before running large-scale experiments.

## Entry Conditions

- Validated research statement and novelty gap (from Lit Review)
- Evidence map with identified baselines, datasets, and methods
- Primary metric tentatively chosen

## Step-by-Step Protocol

### Step 1: Sharpen the Hypothesis

Convert the research statement into a **testable hypothesis**:

```
HYPOTHESIS TEMPLATE
- Claim: [method X] [improves/changes/enables] [metric Y] on [data Z]
         compared to [baseline B] under [conditions C].
- Direction: [X > B by at least D] OR [X ≠ B] OR [mechanism M explains effect]
- Scope: [in-domain / cross-domain / cross-lingual / deployment-like / mechanistic]
- Null hypothesis: [there is no difference / the mechanism does not explain the effect]
```

### Step 2: Define Variables and Controls

**Independent variables** (what you manipulate):
- List each factor and its levels (e.g., model size: {small, medium, large})

**Dependent variables** (what you measure):
- Primary metric: [one metric that is the headline result]
- Secondary metrics: [clearly labeled as secondary/exploratory]
- Metric definitions: [exact formula, averaging policy, edge cases]

**Controls:**
- **Baseline controls**: strong existing methods run under identical conditions
- **Ablation controls**: your method minus one component at a time
- **Negative controls**: conditions where your method SHOULD NOT work (sanity check)
- **Positive controls**: conditions where improvement is expected to be obvious

**Confounders to address:**
- Hyperparameter tuning budget (same budget for baselines and your method)
- Data leakage (train/test overlap, temporal leakage, test contamination)
- Compute differences (compare at equal compute, not just equal epochs)

### Step 3: Data Plan

```
DATA PLAN
- Dataset(s): [name, source, version, access method]
- License/terms: [what is allowed]
- Population/coverage: [what does this data represent? what is missing?]
- Size: [train/val/test counts]
- Split strategy: [random / stratified / temporal / predefined]
- Leakage prevention: [how you ensure no contamination]
- Preprocessing: [deterministic steps, versioned scripts]
- Dataset documentation: [Datasheet or Data Statement — fill if new dataset]
```

**Critical**: define splits BEFORE looking at test data. If using an existing benchmark,
use the canonical splits. If creating new splits, document the procedure and random seed.

### Step 4: Training and Compute Plan (for ML)

```
COMPUTE PLAN
- Model architecture: [family, size, key design choices]
- Hyperparameters:
  - Fixed (not tuned): [list with values and justification]
  - Tuned: [list with search space, search method, budget]
  - Tuning done on: [validation set ONLY — never test]
- Random seeds: [number of runs per condition, e.g., 5 seeds]
- Hardware: [GPU/TPU type, count, memory]
- Expected runtime: [per run, total]
- Checkpointing: [frequency, what is saved]
- Early stopping: [criterion, patience]
```

### Step 5: Analysis Plan (Pre-Commit)

This is the most important step for rigor — it is your informal preregistration.

```
ANALYSIS PLAN
Primary analysis:
- Compare [method] vs [baselines] on [primary metric]
- Statistical test or comparison method: [e.g., paired bootstrap, Wilcoxon]
- Decision rule: [what constitutes "better"? just point estimate? CI must exclude 0?]

Uncertainty reporting:
- Across seeds: [mean ± std, or CI from N runs]
- Across datasets: [if applicable]
- Visualization: [box plots, violin plots, or distribution histograms]

Multiple comparisons:
- How many comparisons: [N models × M datasets × K metrics]
- Correction: [Bonferroni / Holm / none-but-frame-as-exploratory]

Ablation plan:
- Component 1 removed: expected effect = [...]
- Component 2 removed: expected effect = [...]
- Component N removed: expected effect = [...]

Error analysis plan:
- Slices/subgroups to check: [e.g., by language, by difficulty, by domain]
- Qualitative audit: [N random examples from errors, categorized]
- Behavioral tests: [specific input patterns to probe, CheckList-style]

Exploratory analyses (clearly labeled):
- [anything you want to look at but did not commit to in advance]
```

### Step 6: Reproducibility Artifacts Plan

```
ARTIFACT PLAN
- Code repository: [URL, structure, entry points]
- Environment: [conda yml / pip lockfile / Docker container]
- Experiment tracking: [tool: MLflow / W&B / DVC / etc.]
- Run naming scheme: [e.g., {method}_{dataset}_{seed}_{timestamp}]
- How to map paper tables → run IDs: [documented mapping]
- Data release: [plan or justification for not releasing]
- Model release: [plan or justification for not releasing]
- Expected storage footprint: [for artifacts, checkpoints, logs]
```

### Step 7: Ethics and Risk Review

```
ETHICS REVIEW
- Human subjects: [yes/no — if yes, IRB/ethics review status]
- Identifiable data: [yes/no — if yes, de-identification plan]
- Dual-use concerns: [could this be misused? mitigation plan]
- Environmental cost: [estimated compute carbon footprint if large-scale]
- Model documentation: [Model Card planned if releasing a model]
```

### Artifact Locations

When using the exploration structure, save the locked protocol and plans to:
- `explorations/NNN-slug/protocol.md` — the full locked protocol
- Raw datasets → `shared/data/` (shared, immutable)
- Exploration-specific code → `explorations/NNN-slug/src/`

### Step 8: Lock the Protocol

Once all sections are filled:
1. Write the full protocol using [templates/experiment-protocol.md](../templates/experiment-protocol.md)
2. Save it to the exploration directory (e.g., `explorations/NNN-slug/protocol.md`)
3. Have a collaborator review it (or self-review after 24h)
4. Mark the protocol as LOCKED in the LOGBOX
5. Any deviations from this point forward must be logged as EXPLORATORY

## Exit Criteria

- [ ] Hypothesis is testable with clear direction and scope
- [ ] Variables, controls, and confounders documented
- [ ] Data plan with splits and leakage prevention
- [ ] Compute plan with seed count and hardware specs
- [ ] Analysis plan pre-committed (primary and ablation)
- [ ] Artifact plan with environment and tracking setup
- [ ] Ethics review completed
- [ ] Protocol locked and logged in LOGBOX

## Transition

**Forward → Analysis**: carry the locked protocol. Implementation and execution happen
between design and analysis — the agent should help set up code, configs, and tracking.

**Backward → Lit Review**: if design reveals that a critical baseline or dataset is
missing from the evidence map, return to find it.

**Backward ← Analysis**: if pipeline bugs or data leakage are found during analysis,
return here to fix the protocol and re-run.

**Backward ← Writing**: if reviewers identify missing experiments, return here to design
additional tests.
