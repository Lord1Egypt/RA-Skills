## Description:

京东秒杀频道限时好货查询，仅筛选京东自营商品，好评≥98%品质精选，支持品类搜索、价格筛选、折扣力度排序，手慢无。自动过滤无效标签，智能品类推荐，数据通过腾讯云代理安全转发。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cn-shopping](https://clawhub.ai/user/cn-shopping)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers use this skill to query JD seckill products, filter by keyword or maximum price, sort by price or discount strength, and review returned product information and purchase links. It provides shopping lookup results only and does not place orders, create reminders, or guarantee current prices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to a configured Tencent Cloud proxy.

Mitigation: Install and use the skill only when that proxy routing is acceptable for the user's shopping queries.

Risk: Returned product images and purchase links load from remote URLs.

Mitigation: Review links before opening or sharing them, and rely on the final JD page for current price and purchase details.

Risk: The inspected script contains a fallback proxy token.

Mitigation: The publisher should remove the fallback token, rotate it, and use deployment-provided credentials.

## Reference(s):

- [京东自营秒杀 on ClawHub](https://clawhub.ai/cn-shopping/skills/jd-seckill)
- [京东自营9.9包邮](https://clawhub.ai/cn-shopping/jd-99-baoyou)
- [京东自营超级补贴](https://clawhub.ai/cn-shopping/jd-super-deals)
- [购物比价助手](https://clawhub.ai/cn-shopping/best-price)

## Skill Output:

**Output Type(s):** [text, JSON, markdown, guidance]

**Output Format:** [JSON string containing a human-facing summary and serialized product result data with names, prices, discount fields, image URLs, and purchase URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are paginated at up to 50 items per page and may include remote image URLs and purchase links.]

## Skill Version(s):

0.4.2 (source: server release metadata; artifact frontmatter and _meta.json list 0.4.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
