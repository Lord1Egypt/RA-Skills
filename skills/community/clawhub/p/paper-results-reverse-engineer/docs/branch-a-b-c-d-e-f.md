# Branch-Specific Rules: A (Experiment), B (Survey/Correlational), C (Intervention/RCT), D (Developmental), E (Psychometric), F (Neuroimaging)

This document contains detailed branch-specific rules moved from the main SKILL.md to keep it concise.

---

## Branch B: Survey / Correlational / Mediation / Moderation

Activated when Axis 1 = Survey / Correlational study.

### B1: Cross-sectional Mediation Guardrail

When: cross-sectional survey + mediation/moderation/SEM + all variables same timepoint.

Module E must state:
> "This is a theory-driven statistical mediation model, not equivalent to real temporal process or causal mechanism. Without longitudinal, experimental manipulation, or time-interval data, X→M→Y temporal order cannot be established."

**B1a: Statistical effect term ≠ causal claim**

SEM/PROCESS "direct effect" / "indirect effect" / "total effect" are statistical model terms — not automatically causal errors. Distinguish:

| Layer | Definition | Handling |
|-------|-----------|----------|
| Statistical effect term | PROCESS/SEM output: direct/indirect/total effect | Keep, but label "统计间接效应" with "non-causal" note |
| Causal claim | Title/abstract/discussion using affect/reduce/cause/improve | Prohibit; rewrite as associational |
| Mediation interpretation | Discussion saying "X affects Y through M" | Prohibit; note "temporal order not established" |

### B2: Hypothesis Direction Consistency Check

Check Introduction → Hypothesis → Results → Discussion for directional consistency on mediation/moderation strength. Flag conflicts as:
> "⚠️ hypothesis wording inconsistency / directional inconsistency"

### B3: Conditional Indirect Effect Anomaly Check

For conditional indirect effects, check: Boot effect/SE ratio, CI width, CI crosses zero, SE↔CI proportionality, table formatting. Flag anomalies:
> "⚠️ possible formatting/typographical issue; do not overinterpret."

### B4: Johnson–Neyman Direction Consistency Check

Check J-N threshold significance region direction (above vs below), body text consistency, figure support. Flag directional conflicts.

### B5: Measurement Quality Check

Even for non-psychometric papers using scales + SEM/mediation, Module E must check:
- Cronbach's α (total + subscales) — warn if α < .70
- CFA fit indices — warn if RMSEA > .08 or CFI/TLI < .90
- Subscale reliability priority (B5a): if mediator/moderator uses subdimension, check subdimension α before total scale α

### B6: Low Explained Variance / Small Effect Rule

| Indicator | Threshold | Label |
|-----------|-----------|-------|
| R² | < .05 | very low explained variance |
| R² | < .10 | low explained variance |
| Indirect effect | significant but CI near zero | statistical ≠ practical significance |

### B7: Internal Inconsistency Detection Rule

**B7a: Three-layer conflict writing:**
1. Layer 1 — exact quote of conflicting text + table values
2. Layer 2 — possible explanations (use "可能" — "the most likely explanation is…")
3. Layer 3 — evidence grade + manual verification need

**B7b: Cross-paper template text contamination check:**
Trigger: body text variable names not in Study Profile / not in table / look like another paper's topic. Mark as `⚠️ 模板文本污染` — use table values, not surrounding prose.

**B7c: Sign Consistency Check (5 items):**
1. Path coefficient sign vs text direction
2. Indirect effect sign vs a×b
3. Indirect effect sign vs bootstrap CI direction
4. Interaction term text vs table sign
5. Simple slopes direction vs interaction term direction

### B8: Module B Recommended Structure

1. Common method bias / missing data / assumption checks
2. Descriptive statistics
3. Correlation matrix
4. Measurement model / CFA / reliability
5. SEM or regression main paths
6. Mediation model
7. Moderation model
8. Conditional indirect effects
9. Johnson–Neyman / simple slopes
10. Robustness / sensitivity checks
11. Interpretation boundary

### B9: G0 Source Verification Fields

sample size + exclusion count, sampling method, cross-sectional vs longitudinal, scale names + item counts, reliability (α per scale + subscale), CFA fit indices, correlation matrix critical paths, mediation total/direct/indirect effects + CIs, conditional indirect effects at each moderator level, moderation interaction coefficient + p, R² + F per equation, J-N threshold + significance region direction, text-table inconsistencies, causal wording in title/abstract/discussion.

---

## Branch C: Intervention/RCT

### C1–C6 Intervention Subtype Classification

| Subtype | Criteria | Example Label |
|---------|---------|---------------|
| C1 Clinical RCT | Clinical diagnosis, DSM/ICD, therapy/drug trial | "MBCT vs HEP for TRD" |
| C2 Educational RCT | School/classroom, academic outcomes | "Growth mindset in 65 US high schools" |
| C3 Social-psychological intervention | Belief/attitude change, non-clinical | "Values affirmation exercise" |
| C4 Health behavior intervention | Exercise, diet, smoking cessation | "Text message reminders" |
| C5 Organizational intervention | Workplace, leadership/team | "Leadership training RCT" |
| C6 Digital/online intervention | Self-administered, app/web-delivered | "Online growth mindset module" |

Mixed designs: combine labels (e.g., "Educational / social-psychological online intervention RCT").

### C1: Clinical Intervention RCT Dedicated Rules

See C1a–C1h in SKILL.md for the full specification. Key rules:

- **C1a:** AE/safety check mandatory in Module B + E; absence claims capped at Medium-High confidence (Rule 4)
- **C1b:** Distinguish adverse prognostic effects from adverse events
- **C1c:** Session attendance direction ambiguity → sign-convention ambiguity, severity Important
- **C1d:** Six-layer clinical significance separation (statistical → response → remission → absolute difference → sustained → clinical meaningfulness)
- **C1e:** Active comparator strength identification (waitlist/TAU/placebo/attention/active/structurally-equivalent)
- **C1f:** Module B 14-block structure
- **C1g:** G0 source verification fields (20+ clinical RCT fields)
- **C1h:** Source-check for "active comparator effective" interpretation

---

## Branch E: Psychometric / Clinical Screening Tool Validation

### Rule 1: Psychometric Evidence Taxonomy

Evidence must be stratified, not collapsed to "correlational":
- **1a. Reliability:** internal consistency (α/ω), test-retest (r/ICC), inter-rater (κ/ICC)
- **1b. Criterion Validity / Diagnostic Accuracy:** NOT ordinary correlation — sensitivity, specificity, PPV, NPV, LR+/LR−, ROC/AUC
- **1c. Construct Validity:** convergent, discriminant, known-groups, functional impairment
- **1d. Factorial Validity:** EFA/CFA (do not fabricate if absent)
- **1e. Responsiveness/Sensitivity to Change:** pre-post, MID/MCID

### Rule 2: Diagnostic Wording Guardrail

For screening/severity instruments: "screening and severity measure" not "diagnostic tool"; "criteria-based provisional diagnostic aid" not "standalone diagnostic instrument".

Module E must distinguish: Screening utility → Severity grading → Provisional diagnostic aid → Final clinical diagnosis.

### Rule 3: Cutoff Interpretation Rule

For each cutoff: explain tradeoff logic, use-case differentiation (screening vs confirmatory vs balanced), PPV/NPV prevalence dependency, AUC ≠ single-cutoff performance.

### Rule 4: Classic Scale Validation Rule

Pre-2010 papers: distinguish historical validation standard, current best practice, fatal limitations, and future validation needs. Do not mechanically deduct points using contemporary standards.

### Rule 5: Psychometric Module B Structure

Default 12-block structure: Scale Construction → Sample Characteristics → Reliability → Diagnostic Distribution → Criterion Validity → Cutoff Tradeoff → Construct Validity → Factorial Validity (if reported) → Responsiveness (if reported) → Cross-Sample Replication → Subgroup Robustness → Limitations of Clinical Use.

Prohibited: experimental main-effect/interaction structure, IV→DV headings, treating criterion validity as casual correlation.

### Rule 6: Module D Table-First Rule

Prioritize tables over figures: diagnostic accuracy table → severity/distribution → construct validity → ROC curve → items/scoring → sample characteristics → correlation matrix → factor loading → model fit → effect-size visualization.

### Rule 7: Table Orientation Verification

Verify rows, columns, percentage direction (row/column/within-group), cell value type before interpreting any table.

### Rule 9: Psychometric Source Verification Template

High-risk fields: sample N, validation subsample n, criterion-standard interview type + blinding, scale item count + response scale, total score range, cutoff values + sensitivity/specificity, Cronbach's α per sample, test-retest r + interval, AUC, severity categories, whether EFA/CFA reported, whether clinical diagnosis can be replaced.

---

## Branch F: Neuroimaging / fMRI / EEG

Branch-specific focus: task-phase transitions, multiple-comparison correction mentions, brain-behavior correlation, ROI/electrode/time-window identification.

See main SKILL.md Module D for neuroimaging chart types (brain activation maps, RSA matrices, ERP waveforms, connectome plots).

---

## Branch D: Developmental / Educational

Branch-specific focus: age/group comparisons, longitudinal change descriptions, nesting acknowledgments, measurement invariance. Module B maps to: demographic baseline → age/grade differences → growth trajectory → multilevel structure → robustness.
