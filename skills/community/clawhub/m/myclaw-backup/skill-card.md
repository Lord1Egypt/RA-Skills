## Description:

MyClaw Backup helps an OpenClaw user create, schedule, download, upload, and restore backups of OpenClaw configuration, memory, skills, credentials, channel state, and workspace data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leoyeai](https://clawhub.ai/user/leoyeai)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use this skill to protect, migrate, or recover an OpenClaw instance by creating local backup archives, scheduling recurring backups, and restoring from trusted archives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backup archives can contain bot tokens, API keys, channel credentials, and session history.

Mitigation: Keep archives encrypted or otherwise strongly protected, avoid committing or sharing them, and transfer them only over protected channels.

Risk: Restore and upload paths can affect sensitive OpenClaw state and should not process untrusted archives.

Mitigation: Run restores only from trusted archives, use dry-run before applying a restore, and treat the restore and upload web server paths as needing security fixes before remote use.

Risk: The HTTP backup server can expose sensitive backup operations or tokenized URLs if reachable on an unprotected network.

Mitigation: Do not expose the HTTP server on a network without TLS, use a strong token, and avoid sharing tokenized URLs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leoyeai/skills/myclaw-backup)
- [Publisher profile](https://clawhub.ai/user/leoyeai)
- [MyClaw skills ecosystem](https://myclaw.ai/skills)
- [MyClaw](https://myclaw.ai)
- [OpenClaw Backup - What Gets Saved](references/what-gets-saved.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON snippets, and operational status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local .tar.gz backup files, restore OpenClaw state, start a token-protected local HTTP backup manager, or modify cron scheduling when the user runs the provided scripts.]

## Skill Version(s):

2.0.0 (source: server release metadata; artifact _meta.json reports 1.7.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
