## Description:

Automatic conversation backup system for Obsidian with incremental snapshots, hourly breakdowns, and formatted chat-style markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laserducktales](https://clawhub.ai/user/laserducktales)

### License/Terms of Use:

MIT

## Use Case:

Developers and Clawdbot users use this skill to archive conversation transcripts into an Obsidian vault, including scheduled incremental backups, full snapshots, and hourly markdown breakdowns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive conversation transcripts and writes them to an Obsidian vault.

Mitigation: Run it under a low-privilege account and treat the vault and generated markdown snapshots as sensitive data.

Risk: The installer rewrites scripts using user-provided paths, and unsafe pasted paths could affect scheduled execution.

Mitigation: Inspect install.sh before running it, use trusted local paths only, and verify generated script paths before enabling cron.

Risk: The monitor can send token-status metadata through Telegram when alerts are configured.

Mitigation: Disable Telegram alerting unless it is intentionally needed, and check existing Telegram configuration before running the monitor.

Risk: Scheduled cron execution can repeatedly run misconfigured backup scripts in the background.

Mitigation: Test the scripts manually after configuration and enable cron only after confirming the vault, session, and tracking directories are correct.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/laserducktales/skills/obsidian-conversation-backup)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [markdown, files, shell commands, configuration]

**Output Format:** [Markdown transcripts and shell-based setup or backup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Obsidian-compatible markdown snapshots from local JSONL conversation sessions.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
