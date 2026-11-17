## Description:

Queries JD.com self-operated trending products and returns product rankings that can be filtered by category keyword, maximum price, sorting mode, review threshold, and page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cn-shopping](https://clawhub.ai/user/cn-shopping)

### License/Terms of Use:

MIT-0

## Use Case:

External shopping users can ask an agent to find JD.com self-operated best-selling products, narrow results by category or budget, and compare ranking, price, discount, reviews, images, and purchase links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shopping queries are sent through a Tencent Cloud proxy controlled outside NVIDIA.

Mitigation: Review data-handling expectations before installation and avoid sending sensitive or personal shopping intent through the skill unless the proxy operator is trusted.

Risk: The package exposes a reusable proxy authentication token in code.

Mitigation: Publisher should remove and rotate the shared token and provide scoped runtime secrets instead.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cn-shopping/skills/jd-trending)
- [Publisher profile](https://clawhub.ai/user/cn-shopping)
- [京东自营超级补贴](https://clawhub.ai/cn-shopping/jd-super-deals)
- [京东自营历史最低价](https://clawhub.ai/cn-shopping/jd-lowest-price)
- [购物比价助手](https://clawhub.ai/cn-shopping/best-price)

## Skill Output:

**Output Type(s):** [Text, JSON, Links]

**Output Format:** [JSON string containing a human-readable summary and structured product result data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include product names, prices, coupon prices, discounts, shop and brand names, product tags, image URLs, purchase URLs, categories, recent order counts, review percentages, and scores.]

## Skill Version(s):

0.4.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
