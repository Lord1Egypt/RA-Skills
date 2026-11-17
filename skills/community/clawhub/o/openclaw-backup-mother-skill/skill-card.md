## Description:

Guides an agent through backing up OpenClaw configuration and skills, reinstalling OpenClaw, restoring backups, and verifying the result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stefanferreira](https://clawhub.ai/user/stefanferreira)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and administrators use this skill to plan and execute an OpenClaw backup, fresh installation, restore, and validation workflow for upgrades, migrations, or disaster recovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow includes a one-line remote installer that can execute downloaded code.

Mitigation: Use a verified official installer, prefer pinned packages or checksum/signature validation, and inspect downloaded scripts before running them.

Risk: Wildcard restore commands can extract an unintended backup archive or overwrite existing OpenClaw files.

Mitigation: Specify exact backup filenames, verify archive integrity first, and restore into a temporary staging directory before copying files into ~/.openclaw.

Risk: Fresh install and restore commands can remove or replace a working OpenClaw installation.

Mitigation: Create and verify dual backups, keep originals until restore validation is complete, and test the restore process on a non-production system when possible.

## Reference(s):

- [OpenClaw Backup Quick Reference](references/quick-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/stefanferreira/skills/openclaw-backup-mother-skill)
- [ClawHub Publisher Profile](https://clawhub.ai/user/stefanferreira)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands and a verification shell script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes backup, reinstall, restore, troubleshooting, and verification steps.]

## Skill Version(s):

2.2.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
