## Description:

Work with Obsidian vaults (plain Markdown notes) and automate via obsidian-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[12357851](https://clawhub.ai/user/12357851)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Obsidian users use this skill to locate active vaults and operate on Markdown notes with obsidian-cli. It supports searching, creating, moving, renaming, deleting, and directly editing notes while respecting Obsidian vault conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read, create, move, and delete notes in local Obsidian vaults through obsidian-cli.

Mitigation: Confirm the active vault and exact note path before create, move, or delete operations, and back up important vaults before deletes or bulk edits.

Risk: Using obsidian-cli grants access to Obsidian vault contents.

Mitigation: Install only when granting obsidian-cli access to local vaults is acceptable.

## Reference(s):

- [Obsidian Help](https://help.obsidian.md)
- [ClawHub skill page](https://clawhub.ai/12357851/skills/obsidian-1-0-0-local-backup)
- [Publisher profile](https://clawhub.ai/user/12357851)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires obsidian-cli and access to local Obsidian vault configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
