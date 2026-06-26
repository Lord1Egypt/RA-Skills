# Test Case 6: Branch D — Developmental / Educational Study

## Scenario

User provides a Results section from a developmental psychology paper examining age differences in working memory updating across childhood, adolescence, and young adulthood. The paper uses mixed ANOVA with age group as a between-subjects factor.

This test validates:
1. Three-axis classification correctly identifies Axis 1 = Experiment (developmental subtype)
2. Branch D rules are applied: age/group comparisons, nesting acknowledgment, measurement invariance
3. Module B structure follows D template: demographic baseline → age differences → interaction → robustness
4. Age-related language does not slip into causal claims
5. G0 source verification fields are populated

## Input

```
Results

3.1 Age-Related Differences in Working Memory Updating

To examine developmental changes in working memory updating, we tested 144 participants across three age groups: children (n = 48, M_age = 9.2 years, SD = 0.8, 24 female), adolescents (n = 48, M_age = 14.5 years, SD = 0.9, 25 female), and young adults (n = 48, M_age = 22.1 years, SD = 1.6, 26 female). All participants completed a 2-back working memory updating task with two memory load conditions (low load: 1-back; high load: 2-back).

A 3 (Age Group: children, adolescents, young adults) × 2 (Memory Load: low, high) mixed ANOVA on accuracy revealed a significant main effect of Age Group, F(2, 141) = 28.41, p < .001, ηp² = .29, a significant main effect of Memory Load, F(1, 141) = 64.83, p < .001, ηp² = .32, and a significant Age Group × Memory Load interaction, F(2, 141) = 11.36, p < .001, ηp² = .14.

To decompose the interaction, we examined simple effects of Memory Load within each age group. The load effect was largest in children, F(1, 47) = 43.21, p < .001, ηp² = .48, moderate in adolescents, F(1, 47) = 18.67, p < .001, ηp² = .28, and smallest in young adults, F(1, 47) = 9.84, p = .003, ηp² = .17. Pairwise comparisons (Bonferroni corrected) indicated that children performed significantly worse than adolescents (p = .004) and young adults (p < .001) under high load, while the adolescent–young adult difference was not significant (p = .082). Under low load, only the child–young adult comparison reached significance (p = .031).

A polynomial contrast analysis revealed a significant linear trend of age on high-load accuracy, F(1, 141) = 52.31, p < .001, suggesting progressive improvement in updating capacity across development.

3.2 Controlling for Processing Speed

Because age-related differences in processing speed could confound the working memory findings, we re-ran the analysis with processing speed (digit-symbol substitution task RT) as a covariate. The Age Group × Memory Load interaction remained significant after controlling for processing speed, F(2, 140) = 6.89, p = .001, ηp² = .09, although the effect size was attenuated.

3.3 Measurement Invariance Across Age Groups

To ensure that the working memory task measured the same construct across age groups, we tested measurement invariance using multi-group confirmatory factor analysis. The configural model showed acceptable fit, CFI = .94, RMSEA = .06. The metric invariance model (constrained factor loadings) did not significantly worsen fit, ΔCFI = .008, suggesting that the task measured updating with equivalent meaning across age groups. Scalar invariance was partially supported, ΔCFI = .012, indicating that group mean comparisons should be interpreted with some caution.

3.4 Individual Differences: Age × Fluid Intelligence Interaction

Finally, we examined whether fluid intelligence (Raven's Progressive Matrices) moderated age-related improvements. A hierarchical regression predicting high-load accuracy revealed a significant Age × Fluid Intelligence interaction, β = 0.23, p = .006, ΔR² = .04, indicating that the association between fluid intelligence and updating performance strengthened with age.
```

## Expected Output Structure

After receiving this input, the agent should produce:

### Study Profile / Three-Axis Classification

```
| Axis 1 | Experiment (developmental subtype) | [原文Methods] |
| Axis 2 | Developmental / Cognitive | [原文推断] |
| Axis 3 | Behavioral accuracy | [原文Methods] |
| Primary Branch | Branch D | [基于三轴分类] |
```

### Key Branch D Assertions

#### Must contain

- "Branch D" in classification
- "年龄组" or "Age Group" as between-subjects factor
- "儿童" and "青少年" and "年轻成人" as group labels
- "Age Group × Memory Load interaction" correctly identified
- "linear trend" or "线性趋势" noted
- "measurement invariance" or "测量不变性" in Module B or E
- "加工速度" or "processing speed" covariate analysis noted
- "scalar invariance partially supported" → caveat in Module E
- "F(2, 141) = 28.41" preserved exactly
- "ηp² = .29" format preserved from original
- "n = 48" per group reported
- "3.4 Age × Fluid Intelligence" as individual differences section

#### Must NOT contain

- N taken from df (e.g., N = 141 from denominator df — must use 144 from Methods)
- "年龄导致/引起/造成" causal language
- "developmental trajectory proves..."
- Conflation of cross-sectional age differences with longitudinal change (without noting the design limitation)
- "scalar invariance fully supported" (it was partial)

#### Module B structure check

Expected order for Branch D:
1. Demographic baseline and sample description (3.1)
2. Core age/group differences (3.1: ANOVA + interaction + simple effects)
3. Trend analysis (3.1: polynomial contrast)
4. Robustness/control check (3.2: processing speed covariate)
5. Measurement quality check (3.3: invariance)
6. Individual differences extension (3.4: intelligence interaction)

#### Module E boundary check

- Must note: cross-sectional design → age differences are NOT developmental trajectories
- Must note: scalar invariance only partially supported → mean comparisons need caution
- Age × Intelligence interaction → interaction, NOT "intelligence causes development"

#### G0 Source Verification

- N must be from Methods (144), not from df (141)
- Age stats must match: children M = 9.2, adolescents M = 14.5, adults M = 22.1
- Sex distribution: roughly balanced across groups
