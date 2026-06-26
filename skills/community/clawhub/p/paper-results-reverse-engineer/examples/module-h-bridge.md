# Example: Module H — Writer Transfer Packet

## Trigger

User has generated a standard-mode reverse-engineer output and now requests Module H bridge for use with academic-results-writer.

## Example Module H Output

```markdown
## Module H: Writer Transfer Packet for academic-results-writer

### H1. Target Source Identity
- Paper title: Positive psychology interventions: a meta-analysis of randomized controlled studies
- First author / year: Bolier et al. (2013)
- Source type: pasted Results from PDF
- Section accessed: Results (full)
- Extraction coverage: full
- Reverse-engineer mode used: standard

### H2. Study Design Transfer Summary
- Axis 1 Article Type: Meta-analysis / Systematic Review
- Axis 2 Substantive Domain: Positive Psychology / Health Psychology
- Axis 3 Data/Method Modality: Meta-analytic effect sizes (Cohen's d / Hedges' g)
- Adaptive Branch: G. Meta-analysis
- Match relevance for user writing: High (if user is writing a meta-analysis Results section)
- Reason: same article type, same data modality (pooled ES, heterogeneity, forest plots)

### H3. Results Organization Template

| Target Results block | Function | Evidence from target paper | Transferability | Notes for writer |
|---|---|---|---|---|
| Study selection (PRISMA) | Report literature search results, inclusion flow | "The literature search identified 5,335 records..." → PRISMA flow description | Transfer | Use your own PRISMA numbers; replicate the flow narrative structure |
| Study characteristics | Describe k studies, total N, quality ratings, design features | "The 39 included studies comprised 6,139 participants..." | Transfer | Adapt descriptors to your study set |
| Pooled effect sizes (post-test) | Report main effects for each outcome | "The overall Hedges' g for SWB was 0.34 (95% CI=0.22–0.45, p<.001)" | Transfer | Use your own ES values; replicate: ES → CI → p → I² pattern |
| Heterogeneity | Report and interpret I²/Q | "Heterogeneity was moderate to high (I²=54–67%)" | Transfer | Replicate: report I² → note heterogeneity → if high, discuss implications |
| Follow-up effects | Report longitudinal ES, acknowledge limited data | "At 3–6 month follow-up..." ⚠️ Requires G2 guardrail | Partial | Do NOT directly compare post-test and follow-up d values unless study sets are identical |
| Subgroup/Moderator analyses | Report each moderator separately | Separate forest plots for duration, type, recruitment, quality | Transfer | Do NOT combine moderators into "optimal configuration" (G1 guardrail applies) |
| Publication bias | Report each metric separately | Egger's + fail-safe N + Trim and Fill → per outcome | Transfer | If metrics disagree, report each separately (G6 guardrail) |
| Sensitivity analyses | Report outlier removal effects | "After removing the three largest outliers..." | Transfer | Standard structure |

### H4. Paragraph-Level Writing Pattern
- **Opening sentence pattern:** Topic sentence naming the outcome + brief method recap ("To examine the overall effectiveness of PPIs, we first analyzed the post-test effects on...")
- **Figure/Table invitation pattern:** "As shown in Figure X, the pooled effect..." — integrated into narrative
- **Statistical reporting order:** ES value → CI → p → I² → interpretation
- **Null-result wording:** "did not reach significance (p=.15), though this may reflect reduced statistical power due to..."
- **Marginal-result wording:** "the CI approached but did not cross zero"
- **Closing/boundary sentence pattern:** "However, these findings should be interpreted cautiously given [limitation]"

### H5. Figure/Table Narrative Pattern
- **Figure-first or statistics-first:** Statistics-first (report ES in text, then "as shown in Figure X")
- **Core Figure/Table types:** Forest plot, funnel plot, PRISMA flow, bubble plot (moderator)
- **Caption-to-text strategy:** Caption is technical description; body text adds substantive interpretation
- **Error bar / CI / table interpretation cautions:** CI that crosses zero = "not statistically significant"; CI that approaches zero = "marginally significant"
- **What writer may transfer:** Narrative flow, paragraph structure, reporting pattern
- **What writer must not transfer:** Numerical values, specific findings, author interpretations

### H6. Results–Discussion Boundary
- **Allowed in Results:** ES values, CI, p, I², description of patterns, identification of heterogeneity
- **Must stay in Discussion:** Causal interpretations ("PPIs are effective"), clinical recommendations, comparisons to prior literature, theoretical implications
- **Target paper's boundary style:** Results is relatively contained (mostly statistical reporting); Discussion expands substantially
- **Safer replacement wording for writer:**
  - Instead of "PPIs improved SWB" → "The pooled effect for SWB was d=0.34 (95% CI=0.22–0.45)"
  - Instead of "The effect was robust" → "The effect remained significant after Trim and Fill correction"

### H7. Risk Flags to Pass to academic-results-writer

| Risk | Source module | Severity | Transfer decision |
|---|---|---|---|
| Moderator combination: separate subgroup analyses should not be combined into "optimal configuration" | E (G1 guardrail) | Important | Do not transfer |
| Follow-up effect comparison: post-test and follow-up used different study sets → cannot directly compare d values | E (G2 guardrail) | Important | Do not transfer |
| Publication bias metrics inconsistent across outcomes: Egger's sig for 2/3 outcomes, funnel asymmetry present | E (G6 guardrail) | Important | Transfer with caution — report each metric per outcome |
| Study quality low (mean 5.1/10): pooled effect may overestimate true effect if quality bias exists | E | Important | Transfer with caution — note quality caveat |
| Non-significant moderator interpretation: "stable/universal" wording should be avoided | E (G8 guardrail) | Minor | Transfer with caution — add caveats |

### H8. Recommended academic-results-writer Mode
- Recommended mode: target-paper adaptation
- Suggested output depth: standard-depth
- Whether Source Ledger is needed: yes (to track which patterns are transferred vs modified for user's data)
- Whether design-incompatible handling is needed: no (target and user both meta-analysis)
```

## Chat Summary Addition

```
已附加 Module H: Writer Transfer Packet，可直接复制给 academic-results-writer 的 Target-paper Results Style Adaptation Mode 使用。
```
