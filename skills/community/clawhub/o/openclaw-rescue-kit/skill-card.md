## Description:

OpenClaw rescue toolkit for gateway startup protection, watchdog monitoring, automatic restart, configuration rollback, security hardening, log cleanup, and Git-based configuration versioning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[m17y](https://clawhub.ai/user/m17y)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to install and operate local OpenClaw recovery scripts for gateway health monitoring, restart handling, alerting, safe configuration changes, and cleanup of logs or session state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local automation can restart OpenClaw and kill processes using the configured gateway port.

Mitigation: Review the scripts before installation, test manually first, and avoid automatic scheduling until behavior is understood in the target environment.

Risk: Cleanup and rollback scripts can rewrite configuration history, logs, sessions, memory, and related local files.

Mitigation: Keep independent backups of important OpenClaw state and review cleanup settings before running scheduled maintenance.

Risk: Configured alert webhooks can send information to external services and notify.conf may contain sensitive credentials.

Mitigation: Keep notify.conf private, restrict file permissions, and use only trusted notification endpoints.

Risk: The security guidance states that log-cleaner.sh --dry-run should not be relied on as a safe preview in this version.

Mitigation: Inspect planned cleanup behavior directly and run on disposable or backed-up data before using it on production state.

## Reference(s):

- [OpenClaw Rescue Kit Guide](references/guide.md)
- [OpenClaw Rescue Kit on ClawHub](https://clawhub.ai/m17y/skills/openclaw-rescue-kit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance for installing, scheduling, monitoring, alerting, rollback, hardening, and cleanup scripts.]

## Skill Version(s):

1.11.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
