## Description:

Helps a customer find Pastaclean cleaning products, check prices and shipping, and create unpaid orders for the customer to review and pay.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fabudde](https://clawhub.ai/user/fabudde)

### License/Terms of Use:

MIT-0

## Use Case:

Customers use an agent to search or reorder Pastaclean products, receive a quote, and approve an unpaid order before completing payment themselves.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent could create an unwanted order or exceed the customer's intended spending limits.

Mitigation: Set conservative account limits, show the full quote, and require explicit customer confirmation before every order.

Risk: An exposed account key could allow unauthorized access to the customer's shopping account.

Mitigation: Keep the key in a secret store, never share or log it, and revoke and regenerate it if exposed.

Risk: Retrying a failed order request with a new identifier could create duplicate unpaid orders.

Mitigation: Retry the same order with the same idempotency key and have the customer review the payment link before paying.

## Reference(s):

- [Pastaclean skill on ClawHub](https://clawhub.ai/fabudde/skills/pastaclean)
- [Pastaclean shop](https://www.pastaclean.tv)
- [Pastaclean agent connector](https://www.pastaclean.tv/agent-api/mcp)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Product and shipping quotes, order status, and a payment link for the customer; no agent-side payment.]

## Skill Version(s):

0.1.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
