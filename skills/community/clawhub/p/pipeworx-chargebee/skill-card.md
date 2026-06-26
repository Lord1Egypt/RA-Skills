## Description: <br>
Access and manage Chargebee subscriptions, customers, and invoices with filtering options through a Pipeworx Chargebee API v2 MCP integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b-gutman](https://clawhub.ai/user/b-gutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent inspect or manage Chargebee subscriptions, customers, invoices, billing addresses, and payment methods through the Pipeworx MCP gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects an agent to Chargebee customer, subscription, invoice, billing-address, and payment-method data through a third-party MCP gateway without documented authentication, tenant scope, or data handling. <br>
Mitigation: Install only after confirming who operates the Pipeworx gateway, how Chargebee authentication works, what permissions are granted, and whether the integration is read-only. <br>
Risk: Production customer or payment-related data may be exposed if privacy, retention, or access-control terms are unclear. <br>
Mitigation: Avoid production customer or payment data until privacy, retention, and access-control terms are reviewed and accepted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/b-gutman/pipeworx-chargebee) <br>
- [Pipeworx Chargebee MCP gateway](https://gateway.pipeworx.io/chargebee/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, API calls, configuration] <br>
**Output Format:** [Markdown or text responses from MCP-backed Chargebee operations, plus MCP server configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return customer, subscription, invoice, billing-address, and payment-method data from Chargebee.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
