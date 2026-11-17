## Description:

Config Rollback helps OpenClaw users back up configuration changes, enforce a five-minute restart window, and roll back automatically if Gateway does not return to a running state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[echoflying](https://clawhub.ai/user/echoflying)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill before editing ~/.openclaw/openclaw.json to create a backup, track pending validation items, and recover automatically if Gateway fails to restart within the timeout window.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A recurring user-level cron watchdog can overwrite ~/.openclaw/openclaw.json and restart OpenClaw Gateway.

Mitigation: Install only when that rollback behavior is intended, run it without elevated privileges, review the scripts first, inspect crontab entries after installation, and remove the rollback-guardian cron entry when it is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/echoflying/skills/openclaw-config-rollback)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and shell-script behavior descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces user-facing rollback instructions and configuration-change workflow guidance for OpenClaw.]

## Skill Version(s):

1.0.2 (source: server release metadata, package.json, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
