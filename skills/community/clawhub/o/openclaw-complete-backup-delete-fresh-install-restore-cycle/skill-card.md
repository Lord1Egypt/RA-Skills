## Description:

Guides agents through backing up, deleting, reinstalling, restoring, and verifying an OpenClaw installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stefanferreira](https://clawhub.ai/user/stefanferreira)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators responsible for OpenClaw hosts use this skill to plan and execute backup, clean installation, restore, dashboard verification, and recovery troubleshooting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact delete, reinstall, and global binary replacement steps can remove data or alter host command behavior.

Mitigation: Use the skill only on an isolated or well-backed-up OpenClaw host, validate backups before destructive steps, prefer reversible moves, and confirm every global binary or symlink target before changing /usr/local/bin.

Risk: Credential backup and restore steps copy sensitive OpenClaw credential files.

Mitigation: Encrypt or tightly restrict backup locations and verify restored file permissions before starting services.

Risk: Installer fallback and package steps may execute network-fetched or unpinned software.

Mitigation: Avoid the curl-to-shell fallback where possible, pin and verify packages, and review commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stefanferreira/skills/openclaw-complete-backup-delete-fresh-install-restore-cycle)
- [OpenClaw CLI installer referenced by the skill](https://cli.openclaw.ai/install.sh)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes operational backup, restore, reinstall, verification, and troubleshooting steps for OpenClaw hosts.]

## Skill Version(s):

2.2.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
