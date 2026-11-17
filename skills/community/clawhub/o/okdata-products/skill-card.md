## Description:

What sells, and what do buyers say about it? Searches one page of products for a keyword, then reads one page of reviews for each of the first few, as one table: a row per review with the product's title, price and units sold beside it. Use when the user asks this about Xiaohongshu (RedNote), TikTok, Amazon, AliExpress, Taobao & Tmall, 1688, Douyin Shop. 什么卖得好，买家怎么评价？按关键词搜一页商品，再给排在前面的几个各读一页评价，排成一张表：每条评价一行，旁边带商品标题、价格和销量。

This skill is ready for commercial/non-commercial use.

## Publisher:

[conn-ho](https://clawhub.ai/user/conn-ho)

### License/Terms of Use:

MIT-0

## Use Case:

External users can compare products and buyer feedback across supported commerce platforms using keyword searches and selected product review pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security analysis is partial because path-like references could not be resolved; the skill discloses an external API connection.

Mitigation: Review the references and decide whether the okdata API is acceptable before installing.

Risk: Product and review lookups use paid calls, and a call that reaches a data source is charged even if it fails or returns no results.

Mitigation: State the maximum cost before the first call, set a per-call max_price, and get the user's go-ahead before runs exceeding six calls.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/conn-ho/skills/okdata-products)
- [okdata product search and review guide (English)](https://okdata.online/skills/products/?src=skill-okdata-products)
- [okdata product search and review guide (中文)](https://okdata.online/zh/skills/products/?src=skill-okdata-products)
- [okdata agent setup guide](https://okdata.online/agents.md)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Markdown]

**Output Format:** [Markdown table with product details and reviews, followed by a concise analysis and source note]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses one product-search page and up to five review pages; leaves unavailable fields blank and reports the amount charged and data source.]

## Skill Version(s):

0.2.2 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
