## Description:

AI-native agentic commerce with MCP tools that let agents discover businesses, browse product catalogs with variants, and complete purchases with Stripe payments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theoddbrick](https://clawhub.ai/user/theoddbrick)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers connect an MCP-capable agent to LobsterSearch to search for businesses, compare options, browse live product catalogs, check availability, create orders, obtain Stripe Checkout payment links, and track or cancel orders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The hosted endpoint exposes unauthenticated commerce actions, including draft order creation, payment-link generation, status lookup, cancellation, and refund-capable flows.

Mitigation: Require explicit user approval before order or cancellation actions and verify merchant, item, quantity, price, customer details, payment destination, and refund consequences.

Risk: Agent-provided next_actions can move a shopping session toward purchase or cancellation without enough user review.

Mitigation: Treat next_actions as suggestions, not automatic instructions, and gate each sensitive commerce step with a separate confirmation.

Risk: The security verdict is suspicious because public order and refund-capable tools need careful review before use.

Mitigation: Install only when connecting an agent to a public hosted commerce endpoint is acceptable for the deployment, and apply policy checks around purchase, payment, and cancellation flows.

## Reference(s):

- [LobsterSearch homepage](https://lobstersearch.ai)
- [ClawHub listing](https://clawhub.ai/theoddbrick/skills/lobstersearch-mcp)
- [Publisher profile](https://clawhub.ai/user/theoddbrick)
- [Hosted MCP endpoint](https://mcp.lobstersearch.ai/mcp)
- [Tool schema](artifact/mcp.json)
- [Usage examples](artifact/examples/usage-examples.md)
- [Changelog](artifact/CHANGELOG.md)
- [Smithery listing](https://smithery.ai/server/lobstersearch)

## Skill Output:

**Output Type(s):** [text, JSON, configuration, guidance]

**Output Format:** [Structured MCP tool responses with JSON data, next-action guidance, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Hosted StreamableHTTP MCP endpoint; no authentication required; public rate-limited service]

## Skill Version(s):

0.1.2 (source: server release metadata; artifact frontmatter and changelog describe LobsterSearch MCP server 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
