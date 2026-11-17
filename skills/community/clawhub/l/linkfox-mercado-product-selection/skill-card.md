## Description:

Mercado Libre（美客多）选品数据查询与分析，通过 LinkFox 网关统一调用 24 个商品、官链、关键词、类目、趋势、店铺、评论、汇率与套餐用量工具，覆盖墨西哥、巴西、阿根廷、智利、哥伦比亚站点。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External cross-border e-commerce sellers, marketplace analysts, and agent users use this skill to query Mercado Libre product, catalog, keyword, category, trend, seller, review, exchange-rate, and plan-usage data through LinkFox. It helps users choose products, inspect market demand, compare categories, and retrieve operational data for supported Latin American Mercado Libre sites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles LinkFox API keys and can generate or display account tokens during onboarding.

Mitigation: Treat generated API keys as secrets, avoid pasting them into shell history or shared logs, and rotate or remove keys if they are exposed.

Risk: Custom LINKFOX_* endpoint overrides could send Mercado research queries, account data, or billing actions to an unintended service.

Mitigation: Use the default LinkFox endpoints unless there is an explicit trusted deployment reason to override them.

Risk: Paid Mercado data tools and billing workflows can create charges or payment orders.

Mitigation: Confirm the user's goal before paid calls, review package and payment order details before paying, and do not automatically retry broad paid searches.

Risk: Local response and cache files may contain sensitive product research, account usage, or billing context.

Mitigation: Periodically delete local linkfox response and cache files when they are no longer needed, especially on shared machines or shared workspaces.

Risk: Automatic feedback reporting could disclose more context than intended if used carelessly.

Mitigation: Keep feedback concise and exclude secrets, private data, complete large responses, and sensitive business details.

## Reference(s):

- [Skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-mercado-product-selection)
- [LinkFox Skills](https://skill.linkfox.com/)
- [Mercado Libre Product Selection API Reference](references/api.md)
- [Mercado XP-MCP Tool Reference](references/mercado-tool-reference.md)
- [Authentication and Billing Onboarding](references/onboarding.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API responses and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can save full LinkFox responses and local cache files under a linkfox workspace directory while printing either full JSON or a summarized response.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
