## Description:

Launch and manage the OpenClaw Dashboard web UI for monitoring bots, agents, models, and sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xmanrui](https://clawhub.ai/user/xmanrui)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to install, update, and launch a local dashboard for monitoring bots, agents, models, sessions, gateway health, alerts, and skill inventory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches and runs mutable remote code and installs npm dependencies.

Mitigation: Use pinned releases with checksum or signature verification, and review dependency changes before running the dashboard.

Risk: The skill may stop whatever process is using local port 3000.

Mitigation: Confirm the process using port 3000 before allowing the skill to stop it, especially on shared development machines.

Risk: The dashboard reads the local OpenClaw configuration.

Mitigation: Redact sensitive values and run the dashboard in a trusted local environment with access limited to necessary configuration data.

Risk: Fallback update behavior can delete and re-download the local project directory.

Mitigation: Keep local changes outside the managed project directory or require confirmation before destructive refresh steps.

## Reference(s):

- [OpenClaw Bot Dashboard on ClawHub](https://clawhub.ai/xmanrui/skills/openclaw-bot-dashboard)
- [OpenClaw Dashboard project downloaded by the skill](https://github.com/xmanrui/OpenClaw-bot-review)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration guidance]

**Output Format:** [Markdown response with local and LAN dashboard access URLs plus concise status or error guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run OS detection, process management, project download or update, npm dependency installation, and local development server startup commands.]

## Skill Version(s):

1.0.5 (source: server release evidence and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
