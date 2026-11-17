## Description:

Openclaw Auto Recovery helps agents install, configure, and operate an OpenClaw heartbeat daemon that monitors Gateway connectivity and host resources, sends Feishu alerts, and attempts automatic Gateway recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[u0003-yxuan](https://clawhub.ai/user/u0003-yxuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to deploy and manage OpenClaw heartbeat monitoring, Feishu alerting, and automatic Gateway recovery on hosts running OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The daemon uses persistent automation that can restart OpenClaw Gateway and overwrite OpenClaw configuration during recovery.

Mitigation: Review the scripts before deployment, test recovery behavior in a controlled environment, and keep independent backups of OpenClaw configuration.

Risk: The configuration file is sourced by shell scripts, so untrusted config values can execute code.

Mitigation: Create config.env from trusted input only, restrict file permissions, and review changes before restarting the daemon.

Risk: Feishu and Gateway secrets are required for alerting and health checks.

Mitigation: Protect config.env, rotate exposed credentials, and limit access to the host account running the user systemd service.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/u0003-yxuan/skills/openclaw-auto-recovery)
- [Configuration Reference](references/configure.md)
- [Release Notes](RELEASE.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose persistent systemd user services, local configuration files, and recovery actions that affect an OpenClaw Gateway installation.]

## Skill Version(s):

1.0.7 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
