## Description:

Automated backup to Proton Drive with age-based retention for OpenClaw configs, memory files, content drafts, media, and optional Docker volume backups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to generate shell-command guidance for backing up local OpenClaw workspace data into a Proton Drive sync folder with retention rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The backup scope can include sensitive OpenClaw configuration, memory, agent notes, drafts, media, and optional Docker database volumes.

Mitigation: Review the selected data before running the backup, confirm it is appropriate for the configured Proton Drive account, and avoid Docker volume backups unless they are specifically needed.

Risk: Retention cleanup deletes older copied files from the Proton Drive backup folders.

Mitigation: Review retention expectations before use and test the workflow on non-critical backup data before relying on it.

Risk: The script assumes a specific local Proton Drive sync-folder path.

Mitigation: Confirm the Proton Drive desktop app is installed and adjust the sync-folder path before execution when the local account path differs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nissan/skills/proton-drive-backup)
- [Publisher profile](https://clawhub.ai/user/nissan)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local backup guidance for a Proton Drive sync-folder workflow; optional Docker backup behavior is enabled only when requested.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
