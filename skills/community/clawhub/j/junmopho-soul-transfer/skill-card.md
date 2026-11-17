## Description:

Soul Transfer helps an agent create and restore local backups of OpenClaw agent files, configuration, memory, credentials, sessions, and workspace data using portable archives and integrity checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[junmopho](https://clawhub.ai/user/junmopho)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to migrate an agent between local environments by backing up its identity, memory, skills, configuration, credentials, sessions, and workspace files, then restoring them with verification and rollback steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backup archives can contain credentials, tokens, sessions, memory, and workspace data, so a copied or shared archive may expose sensitive access.

Mitigation: Treat archives like password vaults: keep them local, store them encrypted, inspect contents before restore, avoid archives from untrusted sources, and rotate credentials after migration where practical.

Risk: Restore steps can overwrite current OpenClaw and workspace state and may reinstall dependencies from restored workspace content.

Mitigation: Verify archive integrity, create a safety backup before restore, use dry-run behavior when available, inspect restored workspace contents before dependency installation, and confirm path mappings for the target environment.

## Reference(s):

- [Agent Clone - Restore Reference](references/restore.md)
- [ClawHub Skill Page](https://clawhub.ai/junmopho/skills/junmopho-soul-transfer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe file manifests, checksums, archive paths, verification results, restore steps, and rollback guidance.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
