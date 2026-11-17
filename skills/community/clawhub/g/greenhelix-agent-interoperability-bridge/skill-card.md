## Description:

A practical Markdown guide for building protocol bridges between GreenHelix agents and x402, ACP, A2A, MCP, Visa TAP, Google AP2/UCP, PayPal Agent Ready, and OpenAI ACP ecosystems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent-commerce engineers use this guide to design GreenHelix interoperability bridges for payment, identity, task, tool, and event flows across major agent protocols. It is reference material with illustrative Python examples, not an executable skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Production-labeled payment and webhook examples could lead to insecure financial integrations if copied directly.

Mitigation: Treat the guide as reference material and add strong request authentication, provider webhook signature verification, replay protection, authorization checks, explicit user payment approval, and scoped credentials before deployment.

Risk: Webhook and cross-protocol event forwarding examples can expose systems to spoofed events, unsafe destinations, or excessive event data sharing.

Mitigation: Validate webhook signatures, allowlist webhook destinations, block private-network egress, and minimize forwarded event data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mirni/skills/greenhelix-agent-interoperability-bridge)
- [GreenHelix sandbox](https://sandbox.greenhelix.net)
- [GreenHelix API](https://api.greenhelix.net/v1)
- [GreenHelix API documentation](https://api.greenhelix.net/docs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guide with illustrative Python code examples and environment-variable notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executing reference material; examples reference WALLET_ADDRESS, AGENT_SIGNING_KEY, and STRIPE_API_KEY credentials supplied by the user environment.]

## Skill Version(s):

1.3.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
