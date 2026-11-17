## Description:

OpenClaw Config Reference helps agents answer questions and troubleshoot issues involving openclaw.json configuration, gateway settings, channels, agents, sessions, sandboxing, tools, browser, models, environment variables, cron jobs, and hooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yixn](https://clawhub.ai/user/yixn)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw operators use this skill to look up openclaw.json schema details, apply safer configuration changes, and recover from gateway startup failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Applying incorrect openclaw.json keys or partial edits can prevent the Gateway from starting.

Mitigation: Back up the config first, prefer validated CLI changes, check JSON syntax, and run openclaw doctor after edits.

Risk: Exposing the Gateway beyond loopback without authentication can create unwanted external access.

Mitigation: Keep the Gateway loopback-only by default and require authentication before intentionally using LAN, webhook, or Funnel exposure.

Risk: Open DM policies combined with elevated tools can give untrusted chat users powerful agent access.

Mitigation: Use pairing or allowlists for direct messages and keep elevated tools disabled unless the deployment is trusted and controlled.

Risk: Injecting the full shell environment into agents can expose secrets more broadly than intended.

Mitigation: Avoid shellEnv: true unless agents require it, and prefer narrowly scoped environment variables for provider keys and runtime settings.

## Reference(s):

- [OpenClaw Config Reference](SKILL.md)
- [Gateway Configuration Reference](references/gateway.md)
- [Agents Configuration Reference](references/agents.md)
- [Channels Configuration Reference](references/channels.md)
- [Session, Sandbox, Cron & Hooks Reference](references/session.md)
- [Tools, Browser & Skills Configuration Reference](references/tools.md)
- [Models & Environment Configuration Reference](references/models-env.md)
- [Troubleshooting Guide](references/troubleshooting.md)
- [ClawHosters](https://clawhosters.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON5 and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
