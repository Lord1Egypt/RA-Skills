## Description:

Search, read, and manage Stripe account data through Stripe's hosted MCP server. Thin pass-through to Stripe's official MCP; the live tool catalog is whatever that server advertises. Use when the user asks about Stripe payments, customers, products, prices, invoices, subscriptions, refunds, balances, or documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick](https://clawhub.ai/user/maverick)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Stripe account operators use this skill to inspect Stripe payments, customers, products, prices, invoices, subscriptions, refunds, balances, and related documentation, and to manage account data when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stripe account access can expose sensitive customer and payment data or make financial and billing changes.

Mitigation: Use a sandbox first, limit credentials to the account and operations needed, and review each proposed financial change before authorizing it.

Risk: The available tool catalog and its instructions can change because they are supplied by Stripe's live MCP server.

Mitigation: Discover the live tool catalog and server-published instructions before use, then confirm the intended operation with the user before any change.

## Reference(s):

- [Stripe MCP documentation](https://docs.stripe.com/mcp)
- [Stripe restricted API keys](https://docs.stripe.com/keys/restricted-api-keys)
- [mcporter configuration reference](https://github.com/openclaw/mcporter/blob/main/docs/config.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Natural-language responses and structured Stripe account data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Account information reflects live Stripe data; available MCP tools may change over time.]

## Skill Version(s):

1.0.5 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
