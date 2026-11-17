## Description:

促销方案测算虾 models discount, full-reduction, gift-cost, break-even, and batch SKU promotion scenarios to estimate profit impact before a campaign decision.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tujinsama](https://clawhub.ai/user/tujinsama)

### License/Terms of Use:

MIT-0

## Use Case:

Ecommerce merchants, operators, and agents supporting them use this skill to calculate gross profit, net profit, break-even discounts, expected total profit, and side-by-side discount scenarios for promotions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Profit estimates can be misleading when default costs, platform fee ranges, return rates, or promotion-lift assumptions do not match the user's real business data.

Mitigation: Review estimated defaults before relying on results, replace them with current merchant data when available, and treat the output as decision support rather than accounting advice.

Risk: Batch mode reads a user-provided CSV file from a local path.

Mitigation: Use only CSV files the user intends the calculator to read, and check the columns and values before running batch analysis.

## Reference(s):

- [成本结构参考模板](references/cost-structure.md)
- [主流电商平台费率参考](references/platform-fees.md)
- [促销效果系数参考](references/promo-effect.md)
- [ClawHub skill page](https://clawhub.ai/tujinsama/skills/promo-calculator-claw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with tables, recommendations, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include numeric profit calculations, break-even thresholds, discount comparisons, risk notes, and optional CSV batch-analysis summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
