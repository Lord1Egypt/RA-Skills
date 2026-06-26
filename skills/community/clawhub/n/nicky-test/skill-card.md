## Description: <br>
Discover and pay Nicky cryptocurrency payment requests on behalf of users, including payment request lookup, asset selection, wallet address generation, transaction reporting, and confirmation polling via REST API and MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michielpost](https://clawhub.ai/user/michielpost) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to inspect and pay Nicky cryptocurrency payment requests, report transaction hashes, and poll payment confirmation status. The normal public payment flow does not require authentication; optional account-level MCP features require a Nicky API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help initiate cryptocurrency payments and wallet transfers. <br>
Mitigation: Require explicit user confirmation before payment actions, and verify the request, asset, destination address, memo, exact amount, and expiration time before funds are sent. <br>
Risk: Optional API-key mode exposes broad Nicky account and credit-transfer controls beyond the public payment flow. <br>
Mitigation: Prefer the unauthenticated public payment flow, and provide NICKY_API_KEY only when the user intentionally needs private account features. <br>
Risk: Payer name and email are sent to Nicky and may be shown to the payment receiver. <br>
Mitigation: Ask the user for payer details, do not invent them, and disclose that those details are shared for payment identification. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/michielpost/nicky-test) <br>
- [Nicky Homepage](https://pay.nicky.me) <br>
- [REST API Reference](references/api.md) <br>
- [MCP Reference](references/mcp.md) <br>
- [OpenAPI Spec for Agents](https://api-public.pay.nicky.me/openapi/agents.json) <br>
- [Nicky MCP Server Card](https://api-public.pay.nicky.me/.well-known/mcp/server-card.json) <br>
- [Agent Integration Guide](https://api-public.pay.nicky.me/agents.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, configuration] <br>
**Output Format:** [Markdown guidance with REST or MCP request details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use NICKY_API_KEY only for optional private MCP account features; the public payment flow does not require authentication.] <br>

## Skill Version(s): <br>
0.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
