## Description:

Guides AI agents through discovering and purchasing x402 or MPP services with the Nevermined Router, from creating a capped spending Delegation and quoting calls to routing requests, reading the ledger, and following buyer guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nevermined-io](https://clawhub.ai/user/nevermined-io)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers and AI agent users use the skill to discover and pay for individual x402 or MPP service calls through Nevermined, within a human-defined spending Delegation, and review the resulting payment ledger.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid routing can update payment settlement, and the security scan reported incomplete reference resolution.

Mitigation: Use the skill only when paid routing is expected; verify the external service, review its references, quote the call, and keep spending within a human-set Delegation cap.

## Reference(s):

- [Router overview](https://nevermined.ai/docs/products/catalog/router/overview)
- [Catalog MCP documentation](https://nevermined.ai/docs/products/catalog/mcp)
- [Buyer identity contract](https://nevermined.ai/docs/products/catalog/router/buyer-identity)
- [Bootstrap and Delegations](references/bootstrap.md)
- [Service discovery](references/discovery.md)
- [Router errors](references/errors.md)
- [Payment ledger](references/ledger.md)
- [Making paid calls](references/paying.md)

## Skill Output:

**Output Type(s):** [API calls, JSON data, Guidance]

**Output Format:** [HTTP request instructions and JSON request/response examples in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate paid external service calls within the Delegation's spending limit.]

## Skill Version(s):

0.1.43 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
