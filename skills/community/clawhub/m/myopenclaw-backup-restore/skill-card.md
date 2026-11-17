## Description:

MyOpenClaw Backup Restore provides cross-platform backup, restore, migration, and browser-based management for OpenClaw state using Node.js.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beyound87](https://clawhub.ai/user/beyound87)

### License/Terms of Use:


## Use Case:

External OpenClaw users and developers use this skill to create portable backups, preview and restore archives, migrate OpenClaw installations across operating systems, and recover from local data loss.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backup archives can contain bot tokens, API keys, session credentials, and other sensitive OpenClaw state.

Mitigation: Store archives securely, transfer them only over encrypted channels, use only backups you created and trust, and rotate any tokens exposed through a backup or server URL.

Risk: The HTTP management server handles credential-bearing archives and can expose backup upload or download paths if published beyond the local machine.

Mitigation: Do not expose the server beyond localhost, always require a strong token, and avoid plain HTTP transfer for backup archives.

Risk: Restore can place persistent code, configuration, credentials, and channel state into ~/.openclaw.

Mitigation: Treat restore as equivalent to installing persistent local state, review archive origin before use, run a dry-run preview first, and keep the automatic pre-restore snapshot.

## Reference(s):

- [OpenClaw Backup - What Gets Saved](references/what-gets-saved.md)
- [ClawHub skill page](https://clawhub.ai/beyound87/skills/myopenclaw-backup-restore)
- [MyClaw.ai](https://myclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown with inline shell commands and generated backup archives]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js; operations read and write ~/.openclaw and may start a token-protected HTTP server when requested.]

## Skill Version(s):

3.0.2 (source: ClawHub release evidence, created 2026-03-07)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
