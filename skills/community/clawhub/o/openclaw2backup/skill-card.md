## Description:

Backs up and restores OpenClaw workspaces, skills, memory files, wallet-related configuration, and settings through quick backup, full backup, selective restore, and backup management workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sucriss](https://clawhub.ai/user/sucriss)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and operators use this skill to create recoverable backups of local OpenClaw environments and restore selected workspace, skill, memory, and configuration data when migrating or recovering an installation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backups can include sensitive wallet, memory, OpenClaw configuration, repository, and workspace data.

Mitigation: Store generated backups in encrypted storage, avoid sharing or syncing unencrypted archives, and review whether wallet, memory, openclaw.json, and .git history should be included.

Risk: Restore and delete operations can overwrite or remove local OpenClaw data.

Mitigation: Use preview or dry-run restore behavior when available and confirm the selected archive, restore scope, and deletion target before running destructive actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sucriss/skills/openclaw2backup)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with PowerShell and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide backup creation, restore, listing, and deletion workflows that read or write ZIP archives and local OpenClaw configuration.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
