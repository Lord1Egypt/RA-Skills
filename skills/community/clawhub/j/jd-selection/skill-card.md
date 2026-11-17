## Description:

京东精选帮助用户按频道、关键词、价格、好评率和排序条件查询京东自营精选商品，并返回商品信息与购买链接。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cn-shopping](https://clawhub.ai/user/cn-shopping)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers use this skill to browse JD shopping channels, compare filtered self-operated products, and narrow recommendations by category, price, quality threshold, sorting mode, and page.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shopping queries are sent to the publisher's Tencent Cloud proxy, and the release ships with a hard-coded shared proxy authentication token.

Mitigation: Install only if that routing is acceptable; the publisher should remove and rotate the embedded token and require a runtime token.

Risk: Broad shopping activation phrasing may route commercial shopping queries unintentionally.

Mitigation: Narrow activation phrasing and review tool invocation behavior before deployment.

## Reference(s):

- [京东精选 ClawHub page](https://clawhub.ai/cn-shopping/skills/jd-selection)
- [淘宝精选](https://clawhub.ai/cn-shopping/taobao-selection)
- [拼多多精选](https://clawhub.ai/cn-shopping/pdd-selection)
- [购物比价助手](https://clawhub.ai/cn-shopping/best-price)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown]

**Output Format:** [JSON string with product result objects and a natural-language Chinese summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include product names, prices, discounts, shop details, tags, image URLs, and purchase URLs; the skill does not place orders.]

## Skill Version(s):

1.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
