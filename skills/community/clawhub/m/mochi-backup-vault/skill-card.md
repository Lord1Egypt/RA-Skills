## Description:

Create content-addressed incremental snapshots, compare versions, verify hashes and restore files into a new directory. Use for Incremental Backup Vault.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT-0

## Use Case:

External agent users and developers can create local incremental backups of selected workspace folders, compare and verify snapshots, and restore verified files into a new directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected folders may contain secrets, and backup data is stored locally without encryption.

Mitigation: Choose source folders carefully, exclude sensitive files, protect the .mochilab directory, and keep it out of public uploads.

Risk: A live database or changing file may not have an application-consistent backup.

Mitigation: Use the database or application’s own consistency-aware backup process before capturing those files.

Risk: Local snapshots can consume workspace disk space.

Mitigation: Monitor disk usage and keep the selected backup scope within the documented size limits.

## Reference(s):

- [Action contract](references/input.md)
- [MochiLab homepage](https://mochilab.bz)
- [ClawHub release](https://clawhub.ai/hznetnewpower/skills/mochi-backup-vault)

## Skill Output:

**Output Type(s):** [Files, JSON, HTML, CSV, Guidance]

**Output Format:** [Local content-addressed backup snapshots, restored files, and JSON, HTML, or CSV reports summarized for the agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Snapshot data and reports are stored in the active workspace; restore writes into a new workspace directory.]

## Skill Version(s):

1.0.1 (source: server-resolved release and metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
