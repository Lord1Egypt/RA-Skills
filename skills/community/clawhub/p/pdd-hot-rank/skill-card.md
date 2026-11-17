## Description:

拼多多实时热销榜好货推荐，覆盖41个品类共707件商品，按销量智能排序，支持关键词搜索、价格筛选、品牌店筛选。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cn-shopping](https://clawhub.ai/user/cn-shopping)

### License/Terms of Use:

MIT-0

## Use Case:

External users can browse Pinduoduo hot-ranking product recommendations, search by keyword or category, filter by price or brand-store status, and sort product lists by sales, score, or price.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a bundled proxy token and can send product search and filter parameters to a configurable network endpoint.

Mitigation: Review the configured proxy endpoint and token handling before installation, and use publisher-managed credentials rather than treating the bundled token as private.

Risk: Product recommendations, prices, sales labels, and purchase links may be incomplete, stale, or shaped by upstream marketplace data.

Mitigation: Treat results as shopping leads and verify product details, final price, seller, coupon, and purchase terms on the destination marketplace before buying.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cn-shopping/skills/pdd-hot-rank)
- [拼多多百亿补贴](https://clawhub.ai/cn-shopping/pdd-baiyi-proxy)
- [拼多多精选](https://clawhub.ai/cn-shopping/pdd-selection)
- [购物比价助手](https://clawhub.ai/cn-shopping/best-price)

## Skill Output:

**Output Type(s):** [text, markdown, API calls]

**Output Format:** [JSON containing human-readable product-list text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include product names, prices, sales labels, category names, image URLs, purchase identifiers, and purchase links returned through the publisher proxy.]

## Skill Version(s):

1.1.1 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
