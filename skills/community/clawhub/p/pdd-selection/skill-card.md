## Description:

拼多多商品搜索、详情查询和频道好货浏览三合一工具，支持百亿补贴/秒杀/销量榜等频道，返回优惠价格、优惠券和购买链接。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cn-shopping](https://clawhub.ai/user/cn-shopping)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to search Pinduoduo products, inspect product details, and browse deal channels such as subsidy, flash-sale, and sales-ranking feeds before deciding what to buy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product searches and product identifiers are sent to a third-party proxy service.

Mitigation: Use the skill only when the publisher and proxy service are trusted for the relevant shopping queries.

Risk: The artifact includes a hard-coded shared proxy token and weak endpoint scoping.

Mitigation: Rotate or remove the embedded token and restrict the proxy destination before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cn-shopping/skills/pdd-selection)
- [拼多多百亿补贴](https://clawhub.ai/cn-shopping/pdd-baiyi-proxy)
- [拼多多实时热销榜](https://clawhub.ai/cn-shopping/pdd-hot-rank)
- [购物比价助手](https://clawhub.ai/cn-shopping/best-price)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [JSON containing Chinese text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes product names, prices, coupon information, sales hints, store/category data, image URLs, and product identifiers when available.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
