## Description:

Backup and restore OpenClaw data, including creating backups, setting up automatic backup schedules, restoring from backup, and managing backup rotation for the ~/.openclaw directory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phenixstar](https://clawhub.ai/user/phenixstar)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and operators use this skill to create, rotate, schedule, and restore backups of local OpenClaw configuration, credentials, workspace data, sessions, and scheduled tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backups may contain credentials, session tokens, private workspace memory, and scheduled tasks.

Mitigation: Store backup archives in an owner-only directory, encrypt them, and avoid shared or synced destinations unless encryption is in place.

Risk: Restore and rollback commands can overwrite or remove the active ~/.openclaw directory.

Mitigation: Make a fresh safety copy before restoring, verify archive contents and target paths, and avoid destructive removal commands unless the target path has been independently checked.

## Reference(s):

- [Restore OpenClaw from Backup](references/restore.md)
- [Project homepage](https://github.com/PhenixStar/openclaw-skills-collection)
- [ClawHub skill page](https://clawhub.ai/phenixstar/skills/phenixstar-openclaw-backup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct creation of compressed local backup archives and backup rotation.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
