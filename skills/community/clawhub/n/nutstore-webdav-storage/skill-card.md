## Description:

Uses Nutstore WebDAV to back up, archive, and restore OpenClaw multi-agent workspace identity files and memory directories, with optional explicit custom path backup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenmuting](https://clawhub.ai/user/chenmuting)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators running OpenClaw workspaces use this skill to configure rclone-backed Nutstore WebDAV backups, run default or scoped backups, check remote backup state, and restore identity or memory data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload workspace data to Nutstore WebDAV without reliably enforcing promised sensitive-file exclusions.

Mitigation: Review and update scripts before real backups to add mandatory rclone filters and explicit rejection of sensitive paths.

Risk: Backup and restore paths may not be fully bounded to the intended agent workspace.

Mitigation: Validate agent names as safe path components, enforce canonical containment for local source and destination paths, and test restores in a separate RESTORE_TARGET_ROOT before using the live workspace.

Risk: Automated cron backups or live restores can affect production workspace data.

Mitigation: Complete dry-run backup and restore checks first, test restoration into a separate RESTORE_TARGET_ROOT, and require explicit confirmation before live path restores.

## Reference(s):

- [Automation setup guidance](references/automation.md)
- [Nutstore and WebDAV notes](references/nutstore-notes.md)
- [rclone Nutstore WebDAV setup](references/rclone-setup.md)
- [Storage scope and exclusion rules](references/storage-scope.md)
- [ClawHub skill page](https://clawhub.ai/chenmuting/skills/nutstore-webdav-storage)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash commands and environment-variable examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash, rclone, WebDAV access, and an OpenClaw workspace; may produce cron examples and backup, check, or restore command invocations.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
