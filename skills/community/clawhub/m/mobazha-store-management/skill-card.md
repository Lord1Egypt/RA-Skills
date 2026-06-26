## Description: <br>
Manage a Mobazha store using MCP tools for products, orders, messages, and settings; requires an active MCP connection through store-mcp-connect. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengzie](https://clawhub.ai/user/fengzie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers and their agents use this skill to manage Mobazha store listings, orders, buyer conversations, discounts, collections, profile details, notifications, rates, wallet receiving accounts, and payment-provider settings through an authenticated MCP connection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated MCP actions can change store listings, order state, messages, discounts, profile data, and storefront settings. <br>
Mitigation: Require explicit seller approval before destructive, financial, or customer-facing actions and summarize proposed changes before execution. <br>
Risk: MCP session tokens and store credentials are sensitive. <br>
Mitigation: Never log or display tokens, and use only an established authenticated MCP connection. <br>
Risk: Refunds, wallet receiving addresses, payment-provider settings, and order lifecycle changes can affect funds or fulfillment. <br>
Mitigation: Review refunds, wallet addresses, provider configuration, and order status changes before approving them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fengzie/mobazha-store-management) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Text, Configuration] <br>
**Output Format:** [Markdown with MCP tool names and JSON parameter examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an authenticated MCP session; sensitive store actions should be reviewed before execution.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
