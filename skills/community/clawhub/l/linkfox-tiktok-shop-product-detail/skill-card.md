## Description:

查询 TikTok Shop 公共商品详情：输入完整商品 URL 或 19 位商品 ID，可指定美国、英国、东南亚及欧洲主要站点，返回标题、类目、价格、销量、SKU 库存、图片、店铺、评论、物流与促销等分组数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and e-commerce operators use this skill to retrieve the current public detail snapshot for one known TikTok Shop product by URL or 19-digit product ID. It is suited for listing audits, SKU and stock checks, price review, product media extraction, and competitor page breakdowns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a LinkFox API key and contacts LinkFox services.

Mitigation: Install and run it only when the LinkFox account and service endpoint are trusted, and treat API keys as secrets.

Risk: Custom LinkFox endpoint environment variables can redirect requests.

Mitigation: Use the default endpoints unless a custom endpoint has been explicitly reviewed and trusted.

Risk: Lookups consume credits, and repeated queries for different products or regions can create additional cost.

Mitigation: Tell the user before additional paid calls and avoid automatic retries or exploratory polling.

Risk: Full API responses are stored locally in the current working directory.

Mitigation: Review stored JSON before sharing it and remove it when it is no longer needed.

Risk: The onboarding helper can create billing orders and the skill can submit feedback.

Mitigation: Review any payment action or feedback submission with the user before allowing it.

## Reference(s):

- [TikTok Shop 商品详情 API 参考](references/api.md)
- [解决认证和积分问题](references/onboarding.md)
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-tiktok-shop-product-detail)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summaries with optional inline JSON excerpts and saved JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script stores the full response under the current working directory and prints either the full JSON response or a summary for large responses.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
