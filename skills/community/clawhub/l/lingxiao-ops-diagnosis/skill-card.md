## Description:

Helps cross-border e-commerce operators diagnose profitability and operations by focusing on net settlement, cancellation, return, delivery-failure reasons, and Lingxiao MCP profit calculators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikeli20221102-ux](https://clawhub.ai/user/mikeli20221102-ux)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce operators and developers use this skill to diagnose why orders are not translating into profit, estimate item-level profitability, and identify whether operational bottlenecks are in pricing, product pages, quality control, logistics, or cash conversion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects to a remote Lingxiao MCP service and may send pricing, cost, shipping, refund, country, and related commercial parameters.

Mitigation: Submit only the minimum commercial parameters needed for the calculation; avoid store credentials, customer records, confidential product plans, and sensitive account data unless the provider's terms and privacy practices have been reviewed.

Risk: The free calculations are single-item static models and can mislead business decisions if treated as full-store analytics or trend analysis.

Mitigation: Use consistent historical data and store-level analytics before making scale, budget, inventory, or market decisions.

## Reference(s):

- [Lingxiao MCP service](https://www.lingxiaochuhai.com/mcp)
- [Lingxiao operations analytics](https://www.lingxiaochuhai.com/tools/analytics)
- [Lingxiao profit calculator](https://www.lingxiaochuhai.com/tools/profit-calc)
- [Lingxiao supply-cost calculator](https://www.lingxiaochuhai.com/tools/supply-cost)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration snippets and structured diagnostic recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose calls to Lingxiao's remote MCP tools for item-level profit and Etsy fee estimates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
