## Description:

Diagnoses and prevents OpenClaw agent operational failures including session bloat, lane deadlocks, bootstrap truncation, auth errors, compaction timeouts, and gateway health issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zurbrick](https://clawhub.ai/user/zurbrick)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to troubleshoot OpenClaw agents that are stuck, slow, failing authentication, hitting provider limits, or approaching operational limits. It also provides preventive guidance for cron lane isolation, bootstrap budget management, session health checks, and failover diagnostics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security review reports unsafe filename handling in session-health-watchdog.sh that could allow crafted local session files to execute code as the user.

Mitigation: Review and patch session-health-watchdog.sh before installing it as a recurring cron job; run scripts manually first and only use the cron watchdog when the sessions directory is not writable by untrusted users or processes.

Risk: Break-glass recovery guidance involves direct edits to OpenClaw state files, which can damage cron configuration if used casually.

Mitigation: Prefer normal OpenClaw commands after restarting the gateway; use direct jobs.json edits only for a fully wedged gateway, with a timestamped backup and JSON validation before restart.

## Reference(s):

- [OpenClaw Operator on ClawHub](https://clawhub.ai/zurbrick/skills/openclaw-operator)
- [Agentic Design Patterns for OpenClaw](references/design-patterns.md)
- [OpenClaw Failure Patterns Catalog](references/failure-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes diagnostic runbooks and optional Bash scripts for local OpenClaw health checks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
