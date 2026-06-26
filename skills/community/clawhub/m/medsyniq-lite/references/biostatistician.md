# Biostatistician -- Full Reference

## Role

Biostatistics specialist with expertise in clinical and epidemiological statistical methods. Provides guidance on study design, hypothesis testing, sample size, survival analysis, meta-analysis, and advanced modeling. Grounded in established theory, regulatory expectations (ICH E9/E9(R1)), and current methodological best practices.

Provides statistical methodology guidance. Does NOT interpret clinical significance -- that is the clinical team's domain.

## Hypothesis Testing -- Test Selection

### Continuous Outcome, Two Groups

- Normal, equal variances: independent t-test
- Normal, unequal variances: Welch's t-test (preferred default)
- Non-normal/ordinal: Mann-Whitney U
- Paired: paired t-test or Wilcoxon signed-rank

### Continuous Outcome, 3+ Groups

- Normal, independent: one-way ANOVA; post-hoc: Tukey HSD (pairwise), Dunnett (vs control)
- Non-normal: Kruskal-Wallis; post-hoc: Dunn's with Bonferroni/Holm
- Repeated measures: RM-ANOVA or linear mixed models (LMM preferred -- handles missing data, unequal spacing)

### Categorical Outcome

- 2x2: chi-square (expected >=5) or Fisher's exact
- RxC: chi-square or Fisher-Freeman-Halton
- Paired: McNemar (2x2), Stuart-Maxwell (RxC)
- Ordered trend: Cochran-Armitage

### Assumptions

- Normality: Shapiro-Wilk (N<50), visual (QQ plot, histogram). Large N: CLT for means.
- Variance: Levene's (robust), Bartlett's (sensitive to non-normality).
- Independence: design issue, not testable post-hoc.

## P-Value -- What It Is and Is Not

IS: P(data this extreme | H0 true).

IS NOT:
- P(H0 is true) -- transposed conditional
- Probability result is "due to chance"
- Measure of effect size or clinical importance
- Fundamentally different at 0.049 vs 0.051

Always report: exact p-value, CI, effect size. A statistically significant but clinically trivial effect is not actionable. A non-significant result with wide CI is inconclusive, not negative.

## Sample Size Formulas

### Two Means (Parallel)
n/group = 2(Z_a/2 + Z_b)^2 * sigma^2 / delta^2

### Two Proportions
n/group = [(Z_a/2 * sqrt(2*p_bar*q_bar) + Z_b * sqrt(p1q1+p2q2))^2] / (p1-p2)^2

### Time-to-Event (Log-Rank)
Events d = 4(Z_a/2 + Z_b)^2 / [ln(HR)]^2
N = d / P(event during study)

### Non-Inferiority
n/group = 2(Z_a + Z_b)^2 * sigma^2 / (delta_NI - delta_expected)^2
One-sided alpha 0.025.

### Cluster-Randomized
Design effect = 1 + (m-1)*ICC
n_cluster = n_individual * design effect

### Adjustments
- Dropout: inflate by 1/(1 - dropout rate)
- Unequal allocation (k:1): multiply by (k+1)^2 / (4k)
- Covariates: multiply by (1 - R^2)
- Interim analyses: inflate by alpha spending adjustment

Z-values: alpha 0.05 two-sided: Z=1.96. Power 80%: Z=0.842. Power 90%: Z=1.282.

## Regression Modeling

### Linear (Continuous Outcome)
Assumptions: linearity, independence, homoscedasticity, normal residuals, no multicollinearity.
Diagnostics: residual plots, VIF (>5 concerning, >10 problematic), Cook's distance, Durbin-Watson.
Model selection: a priori clinical model preferred. AIC/BIC for non-nested. Avoid stepwise.

### Logistic (Binary Outcome)
OR with 95% CI. OR != RR when outcome >10%.
EPV: minimum 10-20 events per predictor.
Fit: Hosmer-Lemeshow, calibration plots. Discrimination: C-statistic/AUROC.
Penalized methods (LASSO, Ridge) when EPV marginal.

### Poisson / Negative Binomial (Counts)
Poisson: mean = variance. Check overdispersion.
Negative binomial: handles overdispersion.
Zero-inflated: excess zeros.
Offset: varying exposure time.

### Cox PH (Time-to-Event)
HR: instantaneous rate ratio, constant over time (PH assumption).
Check PH: Schoenfeld residuals, log-log plots.
When violated: stratified Cox, time-varying coefficients, RMST, Fleming-Harrington, landmark.
Competing risks: cause-specific (Cox) vs subdistribution (Fine-Gray).

## Survival Analysis

### Kaplan-Meier
Non-parametric. Handles right-censoring. Median survival + 95% CI.
Comparison: log-rank (PH holds), Wilcoxon/Breslow (weights early), Tarone-Ware.

### Competing Risks
CIF via Aalen-Johansen (NOT 1-KM). Gray's test. Fine-Gray model for CIF covariates. Cause-specific Cox for etiology.

### Landmark Analysis
Avoids immortal time bias. Select clinically meaningful landmark. Exclude events before landmark.

## Meta-Analysis

### Effect Measures
Binary: OR, RR, RD. Continuous: MD, SMD (Hedges' g). Time-to-event: HR.

### Models
Fixed-effect: one true effect, Mantel-Haenszel / inverse variance.
Random-effects: distribution of effects, DerSimonian-Laird, REML, HKSJ.
Default: random-effects for medical meta-analyses.

### Heterogeneity
Cochran's Q (low power few studies, overpowered many). I^2: 25% low, 50% moderate, 75% high. Tau^2: absolute variance.
Prediction interval: always report (range of effects in future settings).

### Publication Bias
Funnel plot. Egger's (continuous), Peters'/Harbord's (binary). Trim-and-fill (sensitivity only).

## Multiple Comparisons

- Bonferroni: alpha/m. Conservative.
- Holm (step-down): more powerful than Bonferroni.
- Hochberg (step-up): more powerful, requires independence/PRDS.
- Benjamini-Hochberg (FDR): for discovery/screening.
- Fixed-sequence: pre-specified order, stop if any fails.
- Graphical (Bretz): alpha recycling, now standard in confirmatory trials.

## Missing Data

Classification (Rubin): MCAR (unrelated to anything), MAR (depends on observed), MNAR (depends on unobserved).

Methods:
- Complete case: only valid under MCAR.
- Multiple imputation: gold standard under MAR. 20-100 datasets, Rubin's rules.
- MMRM: preferred for longitudinal continuous (implicitly MAR).
- IPW: weight by inverse P(observed).
- Pattern-mixture: sensitivity for MNAR.

Required (ICH E9(R1)): tipping point, reference-based imputation, delta-adjusted imputation.

## Red Flags

- P-hacking / data dredging
- Ignoring multiplicity in confirmatory analyses
- Inappropriate subgroup claims (no interaction test, post-hoc)
- Immortal time bias in observational studies
- Informative censoring treated as non-informative
- Overfitting (EPV too low)
- Ecological fallacy in meta-regression
- Stepwise selection
- OR reported as RR for common outcomes
- MCMC non-convergence (R-hat >1.1, poor trace plots)
- Missing >20% without sensitivity analysis

MedSynIQ Lite -- 5 of 27 agents. Full version with 142 skills: medsyniq.com
