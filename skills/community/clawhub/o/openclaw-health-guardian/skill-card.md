## Description:

Monitors OpenClaw Gateway on macOS and automatically restarts it with a 180-second cooldown and a five-restarts-per-hour limit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhilshi](https://clawhub.ai/user/zhilshi)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw operators use this skill to install and operate a macOS LaunchAgent that checks OpenClaw Gateway health, repairs issues, and restarts the gateway when local checks fail.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent background monitoring can automatically repair and restart OpenClaw Gateway, which may mask repeated local failures.

Mitigation: Install only when persistent recovery is desired, review the scripts first, and monitor ~/.openclaw/logs/health-check.log for repeated restart patterns.

Risk: Reset and uninstall workflows can remove local health state and log files.

Mitigation: Back up ~/.openclaw/logs and ~/.openclaw/state before using deletion commands documented by the skill.

Risk: User-writable service and script files can be changed by anything with access to the same account.

Mitigation: Protect ~/.openclaw and ~/Library/LaunchAgents from unwanted edits and install only in trusted user accounts.

## Reference(s):

- [Openclaw Health Guardian on ClawHub](https://clawhub.ai/zhilshi/skills/openclaw-health-guardian)
- [Technical Implementation Details](artifact/references/technical-details.md)
- [Troubleshooting Guide](artifact/references/troubleshooting.md)
- [Safety and Security Information](artifact/SAFETY.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and configuration paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS with OpenClaw installed; installs a user-level LaunchAgent and writes under ~/.openclaw and ~/Library/LaunchAgents.]

## Skill Version(s):

1.0.3 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
