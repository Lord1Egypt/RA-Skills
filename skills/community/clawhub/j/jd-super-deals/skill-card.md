## Description:

查询京东超级补贴频道商品，筛选京东自营、高好评商品，并支持关键词、价格、补贴力度排序和分页浏览。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cn-shopping](https://clawhub.ai/user/cn-shopping)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers use this skill to find JD.com self-operated Super Subsidy products by category, budget, quality threshold, and discount strength. Agents can return product summaries, prices, image URLs, and purchase links for comparison and shopping guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and query parameters are sent through the publisher's Tencent Cloud proxy, and the remote proxy's filtering and data-handling behavior is outside the local skill package.

Mitigation: Review the publisher and proxy trust model before installation, avoid sending sensitive queries, and monitor or restrict outbound access according to deployment policy.

Risk: The package includes a reusable proxy token, which could permit unintended use of the remote service if shared broadly.

Mitigation: Replace the bundled token with a deployment-specific secret where supported and rotate credentials if the package is redistributed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cn-shopping/skills/jd-super-deals)
- [Publisher profile](https://clawhub.ai/user/cn-shopping)
- [京东自营新品首发](https://clawhub.ai/cn-shopping/jd-new-arrivals)
- [京东自营历史最低价](https://clawhub.ai/cn-shopping/jd-lowest-price)
- [购物比价助手](https://clawhub.ai/cn-shopping/best-price)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [JSON string with human-readable summary and product data suitable for Markdown rendering]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Product entries may include names, prices, discount percentages, shop and brand fields, image URLs, purchase URLs, categories, order counts, and good-comment rates.]

## Skill Version(s):

1.2.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
