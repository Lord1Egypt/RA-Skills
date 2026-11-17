## Description:

对多平台商品价格进行聚合分析与风险评估，输出可行动的购买建议，避免伪低价与条件陷阱误导。

This skill is ready for commercial/non-commercial use.

## Publisher:

[long1973m](https://clawhub.ai/user/long1973m)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers and shopping agents use this skill to compare Chinese-market ecommerce offers for a clearly specified product, weighing price, platform conditions, seller type, and risk before purchase decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Risk recommendations may be inaccurate because the security evidence notes a risk-level handling bug.

Mitigation: Treat risk levels as advisory and manually verify important purchase decisions, seller status, and purchase conditions.

Risk: Ecommerce prices and discounts can change quickly or depend on coupons, membership, region, inventory, or time-limited conditions.

Mitigation: Record the collection time and confirm final checkout price, eligibility, shipping, tax, and return terms before acting.

Risk: Comparing different SKUs, configurations, bundles, refurbished items, or gift listings can produce misleading recommendations.

Mitigation: Compare only matching product specifications and exclude offers that are not directly comparable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/long1973m/skills/price-comparison-analyzer)
- [Input data format](references/input_format.md)
- [Price collection guide](references/price_collection_guide.md)
- [Risk assessment rules](references/risk_assessment_rules.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Structured JSON plus concise text or Markdown explanations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default user-facing output is a short recommendation list with warnings; internal output may include price distribution, abnormal-price checks, and risk evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
