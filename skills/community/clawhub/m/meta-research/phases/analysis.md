# Phase: Analysis

## Goal

Execute the pre-committed analysis plan, quantify uncertainty, perform ablations and
error analysis, and determine whether the evidence supports the claim — while maintaining
a clear boundary between confirmatory and exploratory findings.

## Entry Conditions

- Locked experimental protocol exists (from Experiment Design)
- Experiments have been run (or are running) with tracking enabled
- Raw results are available in the experiment tracker

## Step-by-Step Protocol

### Step 1: Sanity Checks (Before Any Analysis)

Run these BEFORE looking at primary results:

```
SANITY CHECKLIST
[ ] Training converged (loss curves look reasonable)
[ ] No NaN/Inf values in outputs
[ ] Baseline reproduces expected performance (within tolerance of published numbers)
[ ] Data loading is correct (spot-check random samples)
[ ] Train/test split integrity (no overlap, correct sizes)
[ ] Random seeds actually produced different runs (check variance > 0)
[ ] Metric computation matches the definition in the protocol
```

If ANY sanity check fails: log the failure in LOGBOX, diagnose, fix, and re-run.
Do NOT proceed to primary analysis with broken infrastructure.

### Step 2: Primary Analysis (Confirmatory)

Execute exactly what was pre-committed in the analysis plan:

1. **Compute primary metric** across all seeds/folds for each condition
2. **Report uncertainty**: mean ± CI (or full distribution)
3. **Apply the decision rule** from the protocol
4. **Run the pre-committed statistical test** (if applicable)

**Reporting format:**
```
| Method    | Dataset | Metric (mean ± CI) | N runs | Beats baseline? |
|-----------|---------|-------------------|--------|-----------------|
| Ours      | D1      | 82.3 ± 1.2        | 5      | Yes (p < 0.01)  |
| Baseline  | D1      | 79.1 ± 0.8        | 5      | —               |
```

**Critical**: report the primary metric for ALL conditions, including failures.
Do not cherry-pick the best seed or the best dataset.

### Step 3: Ablation Study

For each component identified in the protocol:

```
ABLATION RESULTS
| Configuration         | Metric (mean ± CI) | Δ from full model | Component isolated |
|-----------------------|--------------------|--------------------|-------------------|
| Full model            | 82.3 ± 1.2        | —                  | —                 |
| − Component A         | 78.5 ± 1.4        | −3.8               | A contributes ~4pts |
| − Component B         | 81.9 ± 1.1        | −0.4               | B is marginal     |
| − Component A − B     | 76.2 ± 1.6        | −6.1               | A+B interact      |
```

Ablations should answer: "Which parts of our contribution actually matter?"

### Step 4: Error Analysis

**Quantitative error analysis:**
- Slice performance by meaningful subgroups (e.g., by difficulty, by domain, by length)
- Identify where the model fails worst
- Compare failure patterns between your method and baselines

**Qualitative error analysis:**
- Sample N random errors (e.g., 50-100)
- Categorize errors into types
- Look for systematic patterns

**Behavioral tests** (CheckList-style):
- Test specific capabilities: negation, entity swap, paraphrase, etc.
- Test robustness: noise, typos, distribution shift
- Test edge cases identified during design

```
ERROR ANALYSIS SUMMARY
Worst-performing slices: [list with metrics]
Error categories: [type → frequency → example]
Behavioral test results: [capability → pass/fail rate]
Key finding: [1-2 sentences on what the errors reveal]
```

### Step 5: Uncertainty Quantification

Report uncertainty at multiple levels:

**Across-run variance** (from multiple seeds):
- Standard deviation or confidence interval
- Use bootstrap CI if distribution is non-normal
- If variance is very high, this IS a result — report it prominently

**Across-dataset variance** (if applicable):
- Performance on each dataset separately
- Do not only report the average — show the spread

**Calibration** (if model outputs probabilities):
- Calibration curve (reliability diagram)
- Expected Calibration Error (ECE)
- If miscalibrated: apply temperature scaling and report both

**Proper scoring** (if applicable):
- Brier score for binary outcomes
- Log loss for multi-class
- Report alongside discriminative metrics (accuracy, F1, etc.)

### Step 6: Confirmatory vs Exploratory Boundary

**This is the most important discipline in analysis.**

Everything in the pre-committed analysis plan = CONFIRMATORY.
Everything else = EXPLORATORY.

Label them explicitly in your notes and later in the paper:

```
CONFIRMATORY RESULTS:
- [result 1]: pre-committed comparison of X vs Y on metric M
- [result 2]: pre-committed ablation of component A

EXPLORATORY RESULTS:
- [result 3]: post-hoc analysis of performance by input length (not pre-committed)
- [result 4]: additional baseline Z (found during analysis, not in protocol)
```

Exploratory results can be just as interesting — but they must be labeled as such
and interpreted more cautiously. They are hypothesis-generating, not hypothesis-confirming.

### Step 7: Assess Whether the Claim is Supported

Answer these questions honestly:

```
CLAIM ASSESSMENT
1. Does the primary metric support the hypothesis? [yes/no/partially]
2. Is the effect size meaningful (not just statistically significant)? [yes/no]
3. Do ablations confirm the contribution is from our method (not confounders)? [yes/no]
4. Are there important failure modes that limit the claim? [describe]
5. Would we be comfortable if someone tried to replicate this? [yes/no/concerns]
6. What is the honest "headline" of this work? [1 sentence]
```

**If the claim is NOT supported**: this is a valid result. Log it as a negative finding.
Consider whether it is publishable as a negative result or as useful evidence for the
community. Do NOT p-hack, add post-hoc comparisons, or change the primary metric to
find a "positive" result.

### Step 8: Prepare Results for Writing

Organize outputs for the Writing phase:
- Tables: primary results, ablations, error analysis slices
- Figures: learning curves, calibration plots, distribution plots, qualitative examples
- Run ID mapping: which table/figure comes from which tracked run
- Raw numbers: exportable and reproducible from tracked experiments

**Artifact location**: save the consolidated analysis (results, ablations, error analysis,
claim assessment) to `explorations/NNN-slug/analysis.md`.

## Exit Criteria

- [ ] All sanity checks passed
- [ ] Primary analysis completed per pre-committed plan
- [ ] Ablations completed for all identified components
- [ ] Error analysis performed (quantitative + qualitative + behavioral)
- [ ] Uncertainty reported at appropriate levels
- [ ] Confirmatory/exploratory boundary clearly marked
- [ ] Claim assessment completed honestly
- [ ] Results organized and mapped to tracked runs
- [ ] LOGBOX entry recorded (including whether claim is supported)

## Transition

**Forward → Writing**: carry organized results, claim assessment, and run ID mappings.

**Backward → Experiment Design**: if pipeline bugs, data leakage, or ambiguous protocol
issues are found, return to fix and re-run.

**Backward → Lit Review**: if analysis reveals that assumptions from the evidence map
are wrong (e.g., a baseline performs differently than reported), return to investigate.
