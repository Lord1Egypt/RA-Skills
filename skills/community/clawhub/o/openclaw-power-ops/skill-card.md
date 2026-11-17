## Description:

Operate and maintain OpenClaw installations with CLI commands, configuration management, channel, agent, and model setup, security auditing, troubleshooting, and gateway administration guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kapslap](https://clawhub.ai/user/kapslap)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw administrators use this skill to operate installations, manage channels and agents, change model configuration, run security audits, troubleshoot gateway issues, and perform maintenance tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad operational and destructive commands may affect live OpenClaw channels, agents, gateways, credentials, or configuration.

Mitigation: Review commands before execution, confirm destructive actions, and back up configuration before using commands with --fix or delete behavior.

Risk: Token-handling examples can expose credentials if tokens are placed directly in shell commands or stored insecurely.

Mitigation: Use credential stores, environment variables, or tokenFile references where supported, and avoid pasting secrets into reusable shell history.

Risk: Personal environment notes in the artifact may not apply to other installations.

Mitigation: Adapt or remove hard-coded local environment details before applying the guidance to another deployment.

## Reference(s):

- [OpenClaw CLI Cheat Sheet](references/cli-cheatsheet.md)
- [OpenClaw Security Audit Reference](references/security-audit.md)
- [OpenClaw Docs](https://docs.openclaw.ai)
- [OpenClaw CLI Docs](https://docs.openclaw.ai/cli)
- [OpenClaw Channel CLI Docs](https://docs.openclaw.ai/cli/channels)
- [OpenClaw Agent CLI Docs](https://docs.openclaw.ai/cli/agents)
- [OpenClaw Model CLI Docs](https://docs.openclaw.ai/cli/models)
- [OpenClaw Config CLI Docs](https://docs.openclaw.ai/cli/config)
- [ClawHub Skill Page](https://clawhub.ai/kapslap/skills/openclaw-power-ops)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are operator references and should be reviewed before execution in live OpenClaw environments.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
