## Description:

My Coffee helps agents assist users with Luckin Coffee self-pickup ordering, store and product search, payment QR presentation, order-status lookup, pickup-code retrieval after payment, and cancellation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luckin](https://clawhub.ai/user/luckin)

### License/Terms of Use:

Creative Commons Attribution-NoDerivatives 4.0 International

## Use Case:

External users and agents use this skill to handle Luckin Coffee self-pickup workflows, including finding a store, selecting products, creating an order, presenting payment information, checking order status, and canceling orders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a reusable Luckin bearer token for payment-order actions.

Mitigation: Install only when token reuse is acceptable, avoid saving the token unless persistence is needed, and remove any saved token when reuse is no longer desired.

Risk: Location discovery may rely on coarse IP-based location when precise user location is not provided.

Mitigation: Provide store, area, address, or coordinates directly when ordering, and avoid relying on IP-based location for precise store selection.

Risk: Changing the MCP URL could direct order actions away from the expected endpoint.

Mitigation: Prefer the official Luckin MCP endpoint and avoid overriding LUCKIN_MCP_URL unless the endpoint is explicitly trusted.

## Reference(s):

- [My Coffee Skill Page](https://clawhub.ai/luckin/skills/my-coffee)
- [Luckin MCP Open Platform](https://open.lkcoffee.com/mcp)
- [Luckin MCP Endpoint](https://gwmcp.lkcoffee.com/order/user/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and concise user-facing text, with configuration snippets or shell commands when setup is requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include payment QR code links and order details; avoids exposing tokens, raw tool calls, request parameters, logs, or stack traces.]

## Skill Version(s):

0.8.4 (source: frontmatter, manifest.json, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
