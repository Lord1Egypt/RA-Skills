## Description:

AgentOps: Managing AI Agent Fleets in Production is an SRE playbook for AI agent fleets covering provisioning, observability, cost-aware routing, SLA enforcement, scaling patterns, EU AI Act governance, and the Fleet Commander dashboard with detailed Python API examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Platform engineers, SREs, and infrastructure leads use this guide to plan and operate AI agent fleets with provisioning, observability, cost controls, SLA enforcement, scaling, governance, and a Fleet Commander dashboard pattern.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copy-ready examples may mutate fleet, wallet, marketplace, dispute, and audit state through authenticated GreenHelix API calls.

Mitigation: Run examples against sandbox endpoints first, use dry-run modes where available, and require human approval before applying financial, identity, marketplace, dispute, or containment actions to live systems.

Risk: Broad credentials or tool access could allow examples to exceed the intended operational scope.

Mitigation: Use least-privilege credentials, explicit tool allowlists, scoped API keys, and separate credentials per agent or environment.

Risk: Audit and messaging examples may expose secrets, personal data, or sensitive operational context.

Mitigation: Validate request schemas and redact secrets or personal data before writing audit records, sending messages, or sharing reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mirni/skills/greenhelix-agent-fleet-ops)
- [GreenHelix sandbox](https://sandbox.greenhelix.net)
- [GreenHelix API endpoint](https://api.greenhelix.net/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guide with Python and YAML examples, checklists, tables, and architecture diagrams]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executable guide content; examples require review and adaptation before use against live services.]

## Skill Version(s):

1.3.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
