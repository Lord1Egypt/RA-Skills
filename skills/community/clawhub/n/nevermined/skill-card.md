## Description:

Guides agents and developers through Nevermined payment operations and x402-protected TypeScript and Python integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nevermined-io](https://clawhub.ai/user/nevermined-io)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers building AI agents or APIs, and agents operating a Nevermined account, use this skill to manage payment plans, buy access, check credits or revenue, and add x402 payment protection to TypeScript or Python services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The runbook may authorize payment from an endpoint-provided request without checking the merchant, plan, or cost; scan coverage was incomplete.

Mitigation: Before payment, verify the merchant, plan, amount, and spending cap against approved limits. Review unfamiliar payment flows and prefer the sandbox until a live charge is approved.

## Reference(s):

- [Nevermined agent skill guide](https://nevermined.ai/docs/development-guide/build-using-nvm-skill)
- [Autonomous operations reference](references/autonomous-operations.md)
- [x402 protocol reference](references/x402-protocol.md)
- [Payment plans reference](references/payment-plans.md)
- [MCP paywall reference](references/mcp-paywall.md)
- [Nevermined REST API specification](https://api.sandbox.nevermined.app/api/v1/rest/docs-json)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with REST examples, shell commands, and TypeScript/Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instructions and examples for an agent to adapt; the skill itself does not execute code.]

## Skill Version(s):

1.0.16 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
