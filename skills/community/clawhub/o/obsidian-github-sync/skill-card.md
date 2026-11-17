## Description:

Automates GitHub synchronization for an Obsidian vault with conflict detection and notification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leo-zzl](https://clawhub.ai/user/leo-zzl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Obsidian users use this skill to configure git-based backup and synchronization of an Obsidian vault to GitHub, including unattended sync jobs and manual conflict recovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended synchronization can commit and upload private notes or unwanted files from an Obsidian vault.

Mitigation: Use a verified repository, preferably private, and inspect .gitignore and git status before the first push or before enabling scheduled automation.

Risk: Cron or systemd scheduling can continue committing and pushing changes without active review.

Mitigation: Enable scheduled jobs only after manual test runs are understood, and keep clear commands or procedures available to disable the automation.

Risk: Git rebase conflicts can interrupt synchronization and require manual resolution.

Mitigation: Monitor the conflict flag, review git status in the vault, resolve conflicts manually, and rerun synchronization only after the rebase is complete.

## Reference(s):

- [Setup Guide](artifact/references/setup-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/leo-zzl/skills/obsidian-github-sync)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides the agent through environment-variable setup, cron or systemd scheduling, conflict checks, and manual git recovery steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
