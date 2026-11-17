## Description:

Queries JD.com's 9.9 free-shipping shopping channel for JD self-operated products, with filters for category keywords, maximum price, review threshold, sorting, and pagination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cn-shopping](https://clawhub.ai/user/cn-shopping)

### License/Terms of Use:

MIT-0

## Use Case:

External shopping users use this skill to ask an agent for JD self-operated low-priced, free-shipping product recommendations and compare results by category, price, discount, and review threshold. The skill returns product details and purchase links but does not place orders, track prices, or send alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Every query goes through the publisher's Tencent Cloud proxy, and the package contains a reusable proxy token that should be treated as exposed.

Mitigation: Review carefully before installing, avoid sending sensitive personal data in shopping queries, and require the publisher to rotate the shared proxy token and document proxy handling before trusted deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cn-shopping/skills/jd-99-baoyou)
- [cn-shopping Publisher Profile](https://clawhub.ai/user/cn-shopping)
- [京东自营秒杀](https://clawhub.ai/cn-shopping/jd-seckill)
- [京东自营超级补贴](https://clawhub.ai/cn-shopping/jd-super-deals)
- [购物比价助手](https://clawhub.ai/cn-shopping/best-price)

## Skill Output:

**Output Type(s):** [text, JSON, markdown, guidance]

**Output Format:** [JSON response containing a summary plus a JSON-encoded product list; agents may render image URLs as Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Product entries can include name, price, coupon price, discount percent, shop and brand names, tags, image URL, buy URL, categories, 30-day orders, review share, and score.]

## Skill Version(s):

0.4.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
