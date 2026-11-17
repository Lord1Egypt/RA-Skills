## Description:

美团爆单操盘手是面向本地生活商家的美团团购方案设计工具，帮助生成竞对调研、团单设计、分层产品架构、定价折扣模型、活动规划和新店冷启动方案。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikogeyu-cell](https://clawhub.ai/user/mikogeyu-cell)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants, operators, and marketing consultants use this skill to plan Meituan group-buying offers for local service businesses, including competitor research, SKU architecture, coupon economics, activity calendars, compliance checks, and launch reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Merchant operations could use coordinated friends-and-family orders or review solicitation to inflate public sales or review signals.

Mitigation: Remove or revise that tactic before use, and limit launch guidance to bona fide transactions and neutral review requests that follow current Meituan rules.

Risk: Platform promotion rules, coupon sharing, and activity availability can change, especially for medical, oral-care, beauty, and other restricted categories.

Mitigation: Verify current Meituan rules and category eligibility with the merchant account or platform representative before applying discounts, coupons, paid traffic, or activity plans.

Risk: Incorrect price anchors, medical claims, or restricted advertising language could create compliance exposure for merchants.

Mitigation: Check each generated SKU and report against the included compliance checklist, confirm real listed prices, and remove prohibited efficacy claims or unsupported qualification statements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mikogeyu-cell/skills/meituan-baodan)
- [团购方案合规红线清单](artifact/references/compliance.md)
- [美团营销工具规则库](artifact/references/marketing-tools.md)
- [片区竞对调研表模板](artifact/assets/competitor-research-template.md)
- [HTML report skeleton](artifact/assets/html-report-skeleton.html)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown guidance with optional HTML report content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include competitor research tables, SKU cards, pricing calculations, activity calendars, compliance checklists, and an HTML report structure.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
