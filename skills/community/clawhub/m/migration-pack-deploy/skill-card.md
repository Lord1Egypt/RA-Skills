## Description:

Helps a user migrate the Shelby AI assistant between computers by packaging local assistant memory into a zip on the old machine and restoring it on the new machine with user-confirmed paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hechunxian](https://clawhub.ai/user/hechunxian)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to move a local AI assistant profile between machines while preserving assistant memory, identity, habits, and workspace memory through a zip-based pack and restore workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles persistent assistant memory and may copy or overwrite local profile files during restore.

Mitigation: Confirm source and destination paths, review files before overwrite, keep a full backup, and rely on .pre-migration backups for rollback.

Risk: Running deploy.py from an untrusted or unverifiable migration archive can execute unreviewed migration code.

Mitigation: Only run deploy.py from a migration archive the user created or verified, and test with MIGRATE_DEST in an isolated directory before touching the real profile.

Risk: The workflow may direct users to obtain external tools during path repair.

Mitigation: Install required tools only from official verified sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hechunxian/skills/migration-pack-deploy)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell commands and local zip archive paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a local migration zip or restore local assistant memory files after explicit user confirmation.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
