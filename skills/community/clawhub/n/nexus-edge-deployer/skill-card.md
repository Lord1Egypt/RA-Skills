## Description:

Deploy 1-bit quantized AI models on inexpensive VPS infrastructure for Agent-as-a-Service, including unit economics, Hetzner provisioning, Ollama or llama.cpp inference setup, and multi-tenant fleet operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuwanito](https://clawhub.ai/user/shuwanito)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure engineers use this skill to plan, provision, and operate VPS-hosted AI inference for multi-tenant agent deployments. It helps compare model tiers, generate deployment steps, configure inference services, and estimate commercial unit economics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide chargeable cloud provisioning and server configuration.

Mitigation: Use scoped Hetzner credentials and require an explicit reviewed plan plus confirmation before provisioning or changing infrastructure.

Risk: The skill's local-only privacy claim conflicts with its cloud inference fallback guidance.

Mitigation: Disable cloud inference fallback, or require separate approval, when workloads may include private, regulated, or client data.

Risk: Exposed inference endpoints can create unauthorized access paths.

Mitigation: Require authentication, network restrictions, and review of any public endpoint before deployment.

## Reference(s):

- [ClawHub listing](https://clawhub.ai/shuwanito/skills/nexus-edge-deployer)
- [NEXUS AI ROI calculator](https://shuwanito.github.io/nexus-ai/)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with deployment steps, configuration guidance, command examples, and cost analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include infrastructure provisioning plans, monitoring recommendations, and unit economics estimates.]

## Skill Version(s):

2.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
