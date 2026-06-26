# Branch G: Meta-analysis / Systematic Review — Detailed Rules

This document contains the full Branch G specification for meta-analysis and systematic review papers. For neuroimaging coordinate-based meta-analysis, see also the neuroimaging subbranch rules below.

---

## G1: Moderator Combination Guardrail

When meta-analysis reports multiple subgroup/moderator results, **do not combine separate moderator analyses into a "best intervention configuration"** unless the paper performed: multivariate meta-regression, moderator × moderator interaction, or combined subgroup analysis.

All moderators are between-study variables, not within-study randomized manipulations — cannot be directly causal-interpreted.

**Prohibited:**
- "个体治疗 + 临床转介 + 长持续时间 = 最大效应"
- "recommend combining these three features for optimal effects"

**Recommended:** Describe each moderator separately with restriction statement: "These are separate subgroup analyses; moderators are between-study, not within-study randomized."

## G2: Follow-up Interpretation Guardrail

Before comparing post-test and follow-up effects: check whether study sets are the same, whether follow-up k is substantially smaller, whether statistical power is lower, whether attrition bias exists, whether heterogeneity differs.

**Prohibited:** "effect decayed from d=0.34 to d=0.22" or "SWB effect more durable than depression effect" without checking k/N/study-set equivalence.

## G3: Results Heading Detection Rule

Before Module B, scan for explicit headings (bold, numbered, standalone phrases). Always separate "原文显式小节标题" from "Skill 教学性补充分块".

**Prohibited:** "本文 Results 不设小节标题" unless full-text scan confirms zero headings.

## G4: PRISMA Flow Number Rule

Must distinguish records / articles / studies:
- Records identified → after dedup → screened → excluded → full-text assessed → full-text excluded (with reasons) → articles included → independent studies

Never conflate: 5,384 records with 40 articles with 39 studies.

## G5: Meta-analysis Causal Language Rule

RCT meta-analysis: each included study supports causal inference, but cross-study synthesis introduces additional uncertainty (heterogeneity, publication bias, quality differences) → causal language must be grade-lowered.

**Allowed:** "pooled evidence from included RCTs shows small effects on SWB and depression"
**Prohibited:** "proves PPIs are effective" / "proves one protocol is optimal"

## G6: Publication Bias Interpretation Rule

When Egger's test, fail-safe N, funnel plot, and Trim and Fill results are inconsistent: report each metric separately. Do not summarize as "all outcomes show equivalent publication bias."

## G7: Module B Meta-analysis Structure

Default logic blocks: Study selection (PRISMA) → Study characteristics → Pooled effect sizes → Heterogeneity → Follow-up effects → Subgroup/Moderator → Publication bias → Sensitivity analyses.

## G8: Non-significant Moderator Interpretation Rule

Non-significant subgroup differences ≠ "effect is stable/universal." Possible reasons: insufficient power, within-subgroup variability, imprecise operationalization. Add caveats.

---

## Neuroimaging Coordinate-Based Meta-Analysis Subbranch

Triggered by: ALE / SDM / MKDA / BrainMap / NeuroSynth / MACM / coordinate-based meta-analysis.

### G9: Identification Rule

Label as: Branch G — Meta-analysis / Systematic Review, Subbranch: Neuroimaging coordinate-based meta-analysis.

Three-axis classification: Axis 1 = Meta-analysis, Axis 2 = Cognitive neuroscience/fMRI, Axis 3 = Coordinate-based neuroimaging meta-analysis (ALE/SDM/MKDA).

**Prohibited:** labeling as Branch F (single fMRI experiment) or Branch I (methodological simulation).

### G10: ALE Is Not Pooled Effect Size

ALE convergence = spatial consistency of reported activation peaks across studies. Not Cohen's d / Hedges' g. Cluster size / peak T / ALE score ≠ effect size magnitude.

### G11: Functional Decoding Is Not Moderator Analysis

BrainMap BD/PC annotation answers "what psychological processes are typically associated with this brain region?" — not "do study characteristics moderate ALE results?"

### G12: MACM Interpretation Guardrail

MACM = cross-experiment co-activation modeling based on BrainMap database. Not BOLD time-series functional connectivity. Cannot infer directional or causal connectivity. Must note seed experiment count imbalance when comparing VOIs.

### G13: Absence Evidence Caution

Absent BD for a region ≠ "proves the region does not participate in that process." Constrained by BrainMap taxonomy, task classification, and database coverage.

### G14: Coordinate-Label Consistency Check

Mandatory checks: hemisphere label ↔ x coordinate sign, anatomical label ↔ y/z position, table coordinates ↔ text coordinates, OCR negative sign loss.

### G15: Caption-Method Threshold Mismatch

If figure caption threshold symbol contradicts Methods (e.g., FWE > .05 vs p < .05): flag as likely typographical issue. Interpret per Methods. Low-priority manual check.

### G16: Discussion Model Separation Rule

Discussion heuristic/neural/working models must be separated from Results data. Label as `[Discussion heuristic model, not direct Results output]`. Prohibit: "ALE results proved the three-stage model."

### G17: Neuroimaging Meta-Analysis G0 Source Verification Fields

k, N, experiments count, foci count, ALE threshold type + p value, cluster extent threshold, database/search source, number of VOIs, VOI experiment counts per seed, MNI vs Talairach space, Left/Right label ↔ x coordinate sign, cluster anatomical label ↔ MNI coordinate, caption threshold ↔ Methods threshold, heuristic model location, functional decoding method + correction method.
