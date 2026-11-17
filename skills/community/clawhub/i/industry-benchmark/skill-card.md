## Description:

帮助 Amazon 卖家查看 ASIN 在类目中的星级与差评率位置，并按近期热度、差评率或平均星级查看类目排行。

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and product researchers use this skill to compare an ASIN's rating and negative-review rate with its category, view category rankings, and review customer feedback for product positioning.

### Deployment Geography for Use:

Global; supported Amazon marketplaces include the US, UK, Germany, Japan, Canada, France, Spain, and Italy.

## Known Risks and Mitigations:

Risk: Paid collection or analysis may spend account credits without fresh approval; omitting --confirm may not reliably prevent a charge.

Mitigation: Set the account to ask before every charge, use the dedicated quote command for estimates, and approve recurring collection costs separately.

Risk: Conflicting confirmation instructions and a deepdive reporting defect can lead to misleading descriptions of paid execution.

Mitigation: Correct those instructions before relying on them, and verify actual charges and report status from command results.

## Reference(s):

- [Skill release page](https://clawhub.ai/funewa/skills/industry-benchmark)
- [ARI CLI and API reference](artifact/references/reference.md)
- [ARI product portal](https://ari.funewa.com/zh/products)
- [ARI monitoring center](https://ari.funewa.com/zh/monitor)
- [ARI reports](https://ari.funewa.com/zh/reports)

## Skill Output:

**Output Type(s):** [Text, Markdown reports, Analysis and recommendations, CSV data exports]

**Output Format:** [Conversational summaries and Markdown reports; optional CSV, HTML, or Markdown exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Varies with the requested ASIN, marketplace, and report scope.]

## Skill Version(s):

1.5.3 (source: SKILL.md frontmatter, CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
