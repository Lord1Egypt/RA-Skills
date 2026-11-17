## Description:

Precision decisioning, agentic trust, and verifiable identity for autonomous agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[knuckles-stack](https://clawhub.ai/user/knuckles-stack)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agent operators use Openclaw Plugin to verify high-risk OpenClaw tool calls against Kevros governance policy, record post-execution attestations, and query agent trust passports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-risk tool inputs, command arguments, file-operation details, hostname-derived agent IDs, and short output excerpts may be sent to the Kevros gateway.

Mitigation: Use the plugin only in environments where that data sharing is acceptable; configure an explicit agentId and apiKey, restrict highRiskTools, and disable autoAttest when output attestation is not appropriate.

Risk: CLAMP decisions may not enforce constrained actions in the local tool call path.

Mitigation: Do not rely on CLAMP as a hard constraint until the plugin applies constrained actions or fails closed; treat CLAMP responses as requiring review or additional enforcement.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/knuckles-stack/skills/openclaw-plugin)
- [Kevros governance gateway](https://governance.taskhawktech.com)
- [Kevros agent discovery card](https://governance.taskhawktech.com/.well-known/agent.json)
- [Kevros MCP endpoint](https://governance.taskhawktech.com/mcp/)
- [Kevros pricing](https://www.taskhawktech.com/pricing)

## Skill Output:

**Output Type(s):** [JSON, Configuration, Guidance]

**Output Format:** [JSON responses and OpenClaw configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Registers OpenClaw hooks for pre-call verification and post-call attestation, plus callable verification and passport lookup tools.]

## Skill Version(s):

0.3.9 (source: server release metadata, package.json, openclaw.plugin.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
