## Description:

拼多多百亿补贴频道好货推荐，全量仅568件稀缺精选商品，覆盖17个品类，4维好货评分模型智能排序，支持关键词搜索、价格筛选、品牌店筛选。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cn-shopping](https://clawhub.ai/user/cn-shopping)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping-assistant agents use this skill to browse 拼多多百亿补贴 products, search by keyword or category, filter by price and brand-store status, and review ranked product information before visiting purchase links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and filters are sent to a cloud proxy.

Mitigation: Review remote data handling before installation and avoid sensitive queries unless the proxy behavior is documented and acceptable.

Risk: The package contains a shared proxy token and weak endpoint scoping.

Mitigation: Prefer a version that removes embedded shared credentials and fixes the proxy endpoint allowlist before broad deployment.

Risk: The skill provides product information and purchase links but does not place orders or verify current checkout terms.

Mitigation: Review product details, price, availability, and seller information in the marketplace before purchase.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cn-shopping/skills/pdd-baiyi-proxy)
- [Publisher Profile](https://clawhub.ai/user/cn-shopping)
- [拼多多实时热销榜](https://clawhub.ai/cn-shopping/pdd-hot-rank)
- [拼多多精选](https://clawhub.ai/cn-shopping/pdd-selection)
- [购物比价助手](https://clawhub.ai/cn-shopping/best-price)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [JSON string containing formatted Markdown product listings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes product names, prices, coupon indicators, sales/category/store metadata, goods_sign identifiers, image URLs, and source attribution when returned by the proxy.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
