## Description:

Guides cross-border ecommerce product selection by classifying category demand drivers, checking market demand, estimating profit, gathering purchase-objection evidence, and deciding whether to launch, test, or pause a product.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikeli20221102-ux](https://clawhub.ai/user/mikeli20221102-ux)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators and product-selection analysts use this skill to evaluate cross-border product opportunities, connect an agent to the Lingxiao MCP service, and structure launch, test, or pause decisions using category, demand, profit, and evidence checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects agents to the Lingxiao MCP endpoint, so product-selection inputs may be shared with that service.

Mitigation: Install and use it only when the organization is comfortable sharing those inputs with Lingxiao.

Risk: Using an API key can expose a trusted provider account flow and may unlock higher limits or paid data tools.

Mitigation: Use an API key only when the provider account, limits, and paid-tool access are approved for the intended workflow.

Risk: Profit and market guidance can be misleading if users treat unavailable data combinations as proof of no demand or omit refund and after-sales costs.

Mitigation: Review MCP outputs against real market evidence, include refund and support assumptions, and avoid treating missing data as a market conclusion.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/mikeli20221102-ux/skills/lingxiao-product-selection)
- [Lingxiao MCP endpoint](https://www.lingxiaochuhai.com/mcp)
- [Lingxiao MCP membership and API key page](https://www.lingxiaochuhai.com/app/membership?from=mcp-trial)
- [Lingxiao Product Scout web tool](https://www.lingxiaochuhai.com/tools/product-scout)
- [Lingxiao service pricing](https://www.lingxiaochuhai.com/service-pricing)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, API Calls, Configuration]

**Output Format:** [Markdown with JSON configuration snippets and MCP tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may depend on Lingxiao MCP responses and user-supplied product category, target country, cost, price, weight, and channel assumptions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
