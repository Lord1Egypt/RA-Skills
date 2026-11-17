## Description:

Precision decisioning, agentic trust, and verifiable identity for autonomous agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[knuckles-stack](https://clawhub.ai/user/knuckles-stack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this plugin to route high-risk OpenClaw tool calls through Kevros governance for verification, attestation, trust passport lookup, and provenance-oriented audit workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-risk tool inputs and short output excerpts are sent to the Kevros gateway.

Mitigation: Install only if the gateway is trusted, avoid sending secrets in governed tool calls, and disable autoAttest unless remote provenance is required.

Risk: An unset API key can trigger implicit remote signup and tie usage to the configured agent identifier.

Mitigation: Set an explicit KEVROS_API_KEY and use a pseudonymous agentId before deployment.

Risk: The security evidence reports a policy-enforcement gap around constrained actions.

Mitigation: Do not rely on CLAMP behavior until constrained actions are applied or blocked as expected; review enforcement behavior before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/knuckles-stack/skills/kevros)
- [ClawHub Publisher Profile](https://clawhub.ai/user/knuckles-stack)
- [NPM Package](https://www.npmjs.com/package/@kevros/openclaw-plugin)
- [Kevros Governance Gateway](https://governance.taskhawktech.com)

## Skill Output:

**Output Type(s):** [JSON, Guidance, Configuration]

**Output Format:** [JSON tool responses, hook allow/block decisions, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The plugin may block high-risk tool calls and can attest truncated output summaries when autoAttest is enabled.]

## Skill Version(s):

0.4.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
