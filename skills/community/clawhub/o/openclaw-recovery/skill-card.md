## Description:

OpenClaw Recovery installs cross-platform backup and health-monitoring automation that checks OpenClaw, repairs invalid configuration values, rolls back to known-good backups, and sends local notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yoyoyosan](https://clawhub.ai/user/yoyoyosan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to keep a local OpenClaw gateway available by scheduling health checks, backups, configuration repair, and rollback across macOS, Linux, and Windows environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs persistent scheduled jobs that can change OpenClaw configuration and restart the gateway without manual approval.

Mitigation: Review the scheduled cron or Task Scheduler entries before installation and confirm the uninstall path removes only the intended OpenClaw recovery jobs.

Risk: The skill backs up authentication-related files, and the security summary flags unsafe handling of those backups.

Mitigation: Restrict backup directory permissions, avoid sharing backup archives, and rotate credentials if backup contents may have been exposed.

Risk: Automatic recovery can overwrite the active OpenClaw configuration during repair, rollback, or safe-mode startup.

Mitigation: Keep a separate known-good configuration copy and test manual backup and rollback behavior before enabling unattended recovery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yoyoyosan/skills/openclaw-recovery)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON configuration references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May install scheduled jobs, write backups and logs under ~/.openclaw, and modify OpenClaw configuration during recovery.]

## Skill Version(s):

4.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
