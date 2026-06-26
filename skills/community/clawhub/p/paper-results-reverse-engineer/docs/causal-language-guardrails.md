# Causal Language Guardrails — Full Specification

## Causal Language Ladder (by Study Design)

### Cross-sectional / Correlational / Survey
- ✅ 相关、关联、预测、与……有关、解释方差 (correlated, associated, predicted, related to, explained variance)
- ❌ 导致、影响、促进、证明机制、因果效应 (cause, influence, promote, prove mechanism, causal effect)

**Cross-sectional Mediation Special Guardrail:**
- ❌ X leads to Y through M / X causes Y via M
- ❌ M explains the causal mechanism
- ❌ X influences M, which in turn reduces Y
- ❌ Mediation proves mechanism
- ✅ The association between X and Y is partially statistically indirect via M
- ✅ The model is consistent with theoretical mechanism, but temporal order cannot be established
- ✅ This is cross-sectional indirect effect evidence
- ✅ Causal mediation requires longitudinal or experimental evidence

### Experimental (random assignment + manipulation)
- ✅ 操纵 X 导致 Y 差异、X 对 Y 有影响 (manipulating X causes Y differences, X has an effect on Y)
- ⚠️ Still note boundary conditions and operationalization limits

### Longitudinal (temporal precedence)
- ✅ X predicts subsequent Y, temporal precedence supports interpretation, baseline X predicts Y change
- ❌ "X causes Y change" from longitudinal alone (without experimental manipulation)

### RCT / Intervention
- ✅ Intervention group showed improvement relative to control, intervention effect significant
- ⚠️ Note attrition, baseline imbalance, blinding limitations

### Meta-analysis
- ✅ Overall evidence shows, pooled effect suggests, moderator analysis indicates, pooled RCT evidence after cross-study synthesis shows
- ✅ Existing evidence supports small-to-moderate effects
- ⚠️ Cannot say "single experimental proof" — individual studies may be RCTs (supporting causal inference), but cross-study synthesis is grade-lowered due to heterogeneity, publication bias, study quality differences
- ❌ Cannot write "single-experiment causal proof," "proves PPIs effective," "proves one protocol optimal"

### Qualitative
- ✅ Themes show, participant narratives reflect, researcher interprets as, patterns emerge
- ❌ Cannot write statistical causation, statistical significance

### Simulation Study / Methodological Comparison
- ✅ Under these simulation conditions, this method under this data-generating mechanism performs, authors suggest, simulation results indicate
- ❌ Proves method X is best, method X is most reliable in all real studies, simulation can directly replace real data, proves an effect does not exist

## Universal Prohibitions (All Non-Manipulation Studies)

- ❌ "证明" (prove)
- ❌ "直接导致" (directly cause)
- ❌ "直接促进" (directly promote)
- ❌ "确定是因为" (determined to be because)

## Recommended Alternatives

- "更支持" (more supportive of)
- "间接支持" (indirectly supports)
- "与……一致" (consistent with)
- "作者偏好的解释" (authors' preferred interpretation)
- "但不构成直接因果证明" (but does not constitute direct causal proof)

## Hypothesis / Result / Interpretation Three-Layer Separation

| Layer | Source | Example |
|-------|--------|---------|
| Hypothesis | Introduction / Results overview | "We predicted that..." |
| Result | Results section data + statistics | "The interaction was significant, F(1,45)=5.23, p=.027" |
| Interpretation | Discussion | "This suggests that..." / "These findings indicate that..." |

**Rules:**
- Never write Discussion interpretation as Results finding.
- Never write exploratory results as a priori hypotheses.
- If paper uses "Intriguingly," "Surprisingly," "Unexpectedly" → flag finding as likely post-hoc/exploratory.
- Correlations are correlations — do not write them as causal mechanisms.

## PPT Three-Layer Separation Rule

Even in oral presentation scripts, maintain layer separation:

- **Result layer:** "结果显示……" / "数据上，[statistic]"
- **Interpretation layer:** "作者在 Discussion 中将其解释为……"
- **Teaching layer:** "汇报时可以理解为……"

**Prohibited PPT sentences:**
- ❌ "CA1 做 pattern completion，CA23DG 做 pattern separation" (Discussion interpretation as Results)
- ❌ "结果证明 CA1 和 CA3 有功能分工" ("证明" prohibited)

## PPT Causal Language Check (for Observational Moderators)

When PPT script uses causal-suggestive words for non-manipulated variables (measured moderators, school classifications): add restriction immediately.

**Words to check when applied to observational variables:**
"导致"、"驱动"、"促进"、"催化剂"、"推动"、"土壤"、"养料"、"种子需要土壤" (metaphorical causal suggestion), "证明"、"证实"

**If variable was randomly manipulated** → causal wording allowed (but still separate Result vs Interpretation).
**If variable was NOT manipulated** → must add: "作者解释为……但该变量未被操纵，不能得出严格因果结论" / "this is an associational pattern only."
**Metaphors (seed and soil)** → can introduce as teaching aid but must follow with causal restriction statement.

## Derived Clinical Metric Labeling Rule

If skill calculates from original data: NNT, NNH, absolute risk difference, relative risk/risk ratio, odds ratio (if not reported), Cohen's d/Hedges' g (if not reported, only means+SD or t/F provided), response rate difference, remission rate difference, percent change/reduction.

Must label: `[Calculated by skill / 教学性计算，非原文直接报告]` — these are teaching approximations, not author-reported exact values.

## Standardized Effect Size Precision Rule

When paper does NOT report standardized effect sizes:
- ✅ "No standardized between-group effect size such as Cohen's d / OR / RR was reported."
- ❌ "No effect size reported." (too vague — paper may report response rate, remission rate, absolute difference etc.)
- Then list what clinical effect information WAS reported.
- Then note which metrics were skill-calculated derivatives.
