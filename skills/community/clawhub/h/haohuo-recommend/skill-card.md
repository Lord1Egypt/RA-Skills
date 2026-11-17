## Description:

电商导购助手，以对话方式为终端买家提供商品推荐、价格查询、优惠提醒、购物建议。基于 haohuo-cps 获取实时商品数据，链接默认为 CPS 推广链接（推广者可赚取佣金）。适合 CPS 推广者接入到自己的 APP 或购物群，作为买家侧的导购入口

This skill is ready for commercial/non-commercial use.

## Publisher:

[zachariah-77](https://clawhub.ai/user/zachariah-77)

### License/Terms of Use:

MIT-0

## Use Case:

External CPS promoters and shopping-service operators use this skill to provide buyer-facing product recommendations, price checks, discount reminders, and purchase guidance based on haohuo-cps product data.

### Deployment Geography for Use:

Mainland China

## Known Risks and Mitigations:

Risk: Buyer-facing recommendations may include affiliate purchase links while suppressing the commission relationship.

Mitigation: Operators should add clear affiliate disclosure and confirm compliance obligations before deploying in buyer-facing settings.

Risk: Product recommendations, prices, discounts, stock, and purchase links depend on haohuo-cps data.

Mitigation: Require current haohuo-cps results before making product claims, and avoid presenting unsupported prices, promotions, availability, or links.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zachariah-77/skills/haohuo-recommend)
- [Haohuo homepage](https://www.haohuo.com)

## Skill Output:

**Output Type(s):** [guidance, markdown, text]

**Output Format:** [Markdown-style conversational shopping recommendations with product summaries, prices, discount notes, and purchase links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Depends on haohuo-cps for product data and should not fabricate product prices, offers, stock, or links.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
