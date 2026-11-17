## Description:

Full CRM with accounts, leads, deals, contacts, pipelines, and work orders - built for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cameron48](https://clawhub.ai/user/cameron48)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and autonomous sales or service agents use this skill to create and update CRM accounts, leads, deals, contacts, pipelines, and work orders through the MCF Agentic gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may send business contacts, sales pipeline details, notes, and work-order information to an external paid CRM gateway.

Mitigation: Configure agents to minimize sensitive data, obtain appropriate consent, and avoid regulated information unless the deployment has approval to submit it.

Risk: Autonomous API use can incur per-call x402 USDC charges on Base L2.

Mitigation: Set budgets, rate limits, and approval controls before enabling automated CRM requests.

## Reference(s):

- [CRM Engine ClawHub listing](https://clawhub.ai/cameron48/skills/mcf-crm-engine)
- [MCF Agentic gateway](https://gateway.mcfagentic.com)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration]

**Output Format:** [Markdown with JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes endpoint paths, per-call pricing, x402 payment posture, and sample payloads.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
