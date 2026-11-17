## Description:

OpenClaw upgrade procedure that guides an agent through environment detection, Windows schtasks or Linux systemd upgrade paths, backup, verification, gateway restart, and rollback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tangsuann](https://clawhub.ai/user/tangsuann)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to perform OpenClaw version upgrades with platform-specific checks for Windows scheduled tasks and Linux systemd environments. It helps sequence compatibility checks, backups, installation, validation, restart, notification, and rollback steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can replace a global OpenClaw package, restart the gateway, inspect local account layout, and create temporary scheduled execution artifacts.

Mitigation: Use it only in environments where those operations are acceptable, and review the planned commands before execution.

Risk: Target version, package registry, and Node.js compatibility issues can leave the gateway unavailable after upgrade.

Mitigation: Pin and verify the target OpenClaw version, registry, and required Node.js engine before installing, then run the documented validation checks before considering the upgrade complete.

Risk: The Windows upgrade path includes a hard-coded user path and temporary scheduled task/script artifacts.

Mitigation: Replace the hard-coded path with the target user's actual OpenClaw path and remove the scheduled task and temporary script after the upgrade.

Risk: Backup files may include .env secrets, and broad permission changes such as chmod 1777 can widen exposure.

Mitigation: Protect or remove .env backups after rollback risk has passed, and avoid broad permission changes unless they are explicitly required and reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tangsuann/skills/oc-upgrade)
- [Publisher profile](https://clawhub.ai/user/tangsuann)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell and PowerShell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes platform-specific operational steps, validation criteria, and rollback guidance.]

## Skill Version(s):

1.9.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
