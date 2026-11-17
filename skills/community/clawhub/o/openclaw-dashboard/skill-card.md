## Description:

OpenClaw operations dashboard for sessions, usage and cost, cron runs, gateway health, DGX Spark work, Local API Hub, and opt-in meeting Copilot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jonathanjing](https://clawhub.ai/user/jonathanjing)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to install, operate, audit, and extend a local OpenClaw dashboard for runtime health, sessions, costs, cron activity, Spark work, and opt-in meeting Copilot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive local operational data could be exposed if the dashboard is shared or compromised.

Mitigation: Keep the dashboard bound to loopback, require a strong OPENCLAW_AUTH_TOKEN, and do not expose it to untrusted networks.

Risk: Security evidence identifies SQL injection, cron file path handling, and DOM XSS issues as unresolved for shared, remote, or multi-user use.

Mitigation: Fix those issues before any shared, remote, or multi-user deployment.

Risk: Copilot and configuration-detail views can increase exposure of audio, provider credentials, or local configuration data.

Mitigation: Leave OPENCLAW_ENABLE_COPILOT and OPENCLAW_ENABLE_CONFIG_ENDPOINT disabled unless needed and review configuration before enabling them.

## Reference(s):

- [OpenClaw Dashboard ClawHub listing](https://clawhub.ai/jonathanjing/skills/openclaw-dashboard)
- [OpenClaw Dashboard homepage](https://github.com/JonathanJing/openclaw-dashboard)
- [Security Model](SECURITY.md)
- [Spark dashboard today schema](refs/spark-dashboard-today-schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose dashboard backend, frontend, documentation, environment, and validation changes for the OpenClaw Dashboard skill.]

## Skill Version(s):

2.0.2 (source: SKILL.md metadata, package.json, CHANGELOG, and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
