## Description:

Discover and pay Nicky cryptocurrency payment requests on behalf of users, covering payment request lookup, asset selection, wallet address generation, transaction reporting, and confirmation polling via REST API and MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michielpost](https://clawhub.ai/user/michielpost)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent discover and pay Nicky cryptocurrency payment requests, report transaction hashes, and poll for payment confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cryptocurrency payments can be misdirected or fail to match if the receiver, asset, exact amount, wallet address, memo, or expiry is wrong.

Mitigation: Before starting or sending a payment, have the user confirm the receiver, asset, quoted amount, wallet address, memo when present, and expiry time.

Risk: Payer name, payer email, payment attempt IDs, and transaction hashes are sent to Nicky and may be visible to the payment receiver.

Mitigation: Ask the user for payer details instead of inventing them, and disclose that those details and transaction identifiers are shared as part of the payment flow.

Risk: The optional private MCP endpoint exposes account-management capabilities beyond simple payment lookup and progress checks.

Mitigation: Use the anonymous public payment flow by default, and provide NICKY_API_KEY only when the user intentionally wants private account-management access.

## Reference(s):

- [Nicky homepage](https://pay.nicky.me)
- [REST API reference](artifact/references/api.md)
- [MCP reference](artifact/references/mcp.md)
- [MCP server card](https://api-public.pay.nicky.me/.well-known/mcp/server-card.json)
- [OpenAPI spec for agents](https://api-public.pay.nicky.me/openapi/agents.json)
- [Full public OpenAPI spec](https://api-public.pay.nicky.me/openapi/v1.json)
- [Interactive API docs](https://api-public.pay.nicky.me/scalar)
- [Agent integration guide](https://api-public.pay.nicky.me/agents.md)
- [Nicky llms.txt](https://pay.nicky.me/llms.txt)

## Skill Output:

**Output Type(s):** [guidance, API calls, shell commands, configuration]

**Output Format:** [Markdown guidance with REST examples and MCP tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include payment details such as receiver, asset, amount, wallet address, memo, expiry, transaction hash, and confirmation status.]

## Skill Version(s):

0.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
