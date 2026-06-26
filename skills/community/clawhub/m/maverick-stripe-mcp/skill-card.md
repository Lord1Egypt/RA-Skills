## Description: <br>
Search, read, and manage Stripe account data through Stripe's hosted MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick](https://clawhub.ai/user/maverick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operators use this skill to inspect Stripe payment data and manage customers, products, prices, invoices, subscriptions, refunds, balances, and related documentation through Stripe's MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change real Stripe account data, including customer, invoice, subscription, refund, balance, and payment information. <br>
Mitigation: Install only when the agent should work with Stripe data, use restricted or test-mode Stripe credentials where possible, and require explicit confirmation before write-capable actions. <br>
Risk: The skill requires the MAVERICK_STRIPE_MCP_ACCESS_TOKEN bearer token. <br>
Mitigation: Store the credential in the runtime secret store or environment, avoid embedding it in code, and rotate or revoke the token if authentication fails or access is no longer needed. <br>
Risk: Write-capable calls can alter billing or money movement state. <br>
Mitigation: Inspect current object state before changing it and require explicit confirmation before creating invoices, issuing refunds, changing subscriptions, or modifying customer or payment data. <br>


## Reference(s): <br>
- [Stripe MCP overview and bearer authentication](https://docs.stripe.com/mcp) <br>
- [Stripe restricted API keys](https://docs.stripe.com/keys/restricted-api-keys) <br>
- [mcporter config reference](https://github.com/openclaw/mcporter/blob/main/docs/config.md) <br>
- [ClawHub skill page](https://clawhub.ai/maverick/maverick-stripe-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON tool-call output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the live Stripe MCP tool catalog as the source of truth for available tools and parameters.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
