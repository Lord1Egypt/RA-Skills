## Description:

香港保险产品数据 API（MCP）：查询/对比储蓄险、寿险、医疗险、危疾险、年金险产品，含真实IRR、回本年、分红实现率数据。Query & compare Hong Kong insurance products (savings/life/medical/critical/annuity) with real IRR, breakeven and dividend fulfillment data via a paid MCP endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newle](https://clawhub.ai/user/newle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, insurance writers, and insurance professionals use this skill to query and compare Hong Kong insurance products through a paid MCP endpoint. It supports product lookup, side-by-side comparison, insurer dividend fulfillment review, and retirement or investment analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a third-party paid insurance-data service and may incur usage charges or quota limits.

Mitigation: Confirm the user accepts the service terms, pricing, and quota behavior before configuring or using the MCP endpoint.

Risk: The skill requires an API key and includes examples for passing bearer tokens to the service.

Mitigation: Store the API key in a protected secret mechanism, avoid pasting raw tokens into chat, and do not hard-code credentials in scripts or shared files.

Risk: The skill mentions optional email CLI handling for verification messages.

Mitigation: Access email only with explicit, narrow user permission for the verification message and avoid broader mailbox inspection.

Risk: Insurance return data can be mistaken for personalized investment or insurance advice.

Mitigation: Present retrieved data as reference information only and direct users to a licensed insurance adviser for purchase decisions or personalized quotes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/newle/skills/hk-insurance-data)
- [HK Insurance Data Website](https://insurance.mytreasure.ren)
- [HK Insurance MCP Endpoint](https://insurance.mytreasure.ren/api/mcp/mcp)
- [Developer Registration](https://insurance.mytreasure.ren/dev/login)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON-RPC examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to retrieve structured Hong Kong insurance product data from a third-party paid MCP service.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
