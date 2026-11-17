## Description:

Guides an agent through configuring bidirectional Obsidian vault synchronization between Mac and iPhone using Syncthing, with optional large-file filtering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ameylover](https://clawhub.ai/user/ameylover)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, knowledge workers, and Obsidian users use this skill to set up peer-to-peer vault synchronization between a Mac and an iPhone without relying on Obsidian Sync or an Obsidian plugin. It also provides guidance for excluding large files to reduce mobile storage usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional rsync helper can copy vault contents to an iCloud destination even though the main setup is presented as a no-iCloud Syncthing workflow.

Mitigation: Review and edit source and destination paths before use, and prefer Syncthing ignore rules when the goal is peer-to-peer filtering only.

Risk: The helper script can modify destination vault data during synchronization.

Mitigation: Run a dry run or test vault first, keep backups, and confirm Syncthing file versioning before using the helper with a live Obsidian vault.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ameylover/skills/obsidian-sync-syncthing)
- [English skill guide](artifact/SKILL.en.md)
- [English README](artifact/README.en.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration]

**Output Format:** [Markdown with setup steps, shell commands, and a Python helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes user-edited filesystem paths and Syncthing configuration values.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
