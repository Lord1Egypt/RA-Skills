## Description:

Administration guide for operating, configuring, and troubleshooting the OpenClaw CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[encryptshawn](https://clawhub.ai/user/encryptshawn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to operate, configure, and troubleshoot OpenClaw CLI installations, agents, routing, model providers, endpoints, secrets, plugins, security checks, backups, and diagnostics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact administration recipes can change agents, services, scheduled jobs, plugins, skills, providers, or cross-agent access.

Mitigation: Review the exact proposed configuration change before applying it, keep scope narrow, and retain explicit confirmation and backup steps.

Risk: Cross-agent memory search or agent-to-agent access can expose another agent's session transcripts or workspace context.

Mitigation: Enable cross-agent access only when needed, document the intended scope, and verify bindings and access rules before use.

Risk: Non-loopback model endpoints and gateway APIs can expose credentials or agent access if placed on an untrusted network.

Mitigation: Use loopback, HTTPS, VPN, or encrypted tunnels for non-local endpoints, and store credentials in environment variables or secret references.

## Reference(s):

- [OpenClaw Admin on ClawHub](https://clawhub.ai/encryptshawn/skills/openclaw-administrator)
- [OpenClaw CLI docs](https://docs.openclaw.ai/cli)
- [Gateway architecture](https://docs.openclaw.ai/concepts/architecture)
- [Multi-agent routing](https://docs.openclaw.ai/concepts/multi-agent)
- [Sub-agents](https://docs.openclaw.ai/tools/subagents)
- [OpenAI HTTP API](https://docs.openclaw.ai/gateway/openai-http-api)
- [Command map](references/command-map.md)
- [Models and providers](references/models-and-providers.md)
- [Multi-agent recipes](references/multi-agent-recipes.md)
- [OpenAI-compatible HTTP API reference](references/openai-http-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include diagnostic sequences, safety checks, and explicit confirmation steps for high-impact administration changes.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
