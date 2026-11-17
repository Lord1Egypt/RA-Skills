## Description:

Production-grade model router for OpenClaw: prefix routing (@codex/@mini), timezone-aware schedule switching, verify-after-switch, rollback, lock protection, and JSONL audit logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vulcanusalex](https://clawhub.ai/user/vulcanusalex)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to route OpenClaw tasks to configured models by explicit prefix or timezone-aware schedule while preserving switch verification, rollback, locking, and audit logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated cron output can become unsafe if a crafted schedule rule ID is installed directly.

Mitigation: Use only trusted schedule files and rule IDs, and do not install cron previews until rule IDs are restricted to a safe character set or shell-quoted.

Risk: Scheduler commands can switch the active OpenClaw model for the account that runs them.

Mitigation: Confirm the OpenClaw CLI, account context, and any configured authentication environment variables before running schedule apply or schedule end commands.

## Reference(s):

- [README](README.md)
- [Model Router Runbook](docs/runbook.md)
- [Scheduler Integration Notes](docs/scheduler-notes.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit JSON route and schedule inspection output, plus JSONL audit logs when the provided commands are run.]

## Skill Version(s):

0.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
