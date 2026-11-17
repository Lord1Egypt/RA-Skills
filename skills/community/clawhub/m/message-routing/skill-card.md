## Description:

Manage how OpenClaw routes Telegram messages to different Claude model backends and switch between CLI and API providers with simple config changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[josephtandle](https://clawhub.ai/user/josephtandle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect and change OpenClaw Telegram routing between Claude CLI and API model providers, including fallback and restore flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Model, fallback, or restore commands can persistently change how Telegram messages are routed and may switch between CLI and API providers.

Mitigation: Back up ~/.openclaw/openclaw.json first and confirm the selected model and provider before applying routing changes.

Risk: Gateway restarts can affect Telegram message processing while routing changes are applied.

Mitigation: Validate configuration with openclaw doctor when needed and check gateway logs after restart.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/josephtandle/skills/message-routing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose persistent OpenClaw routing changes and gateway restarts.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
