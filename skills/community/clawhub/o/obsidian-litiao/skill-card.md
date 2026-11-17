## Description:

Work with Obsidian vaults (plain Markdown notes) and automate via obsidian-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[litiao1224](https://clawhub.ai/user/litiao1224)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Obsidian users use this skill to locate active vaults, search notes, create notes, move or rename notes while preserving common links, delete notes, and make direct Markdown edits when appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can search, edit, move, and delete notes in the selected Obsidian vault.

Mitigation: Ask the agent to confirm the vault and note path before delete, rename, or bulk changes, and keep backups for important vaults.

Risk: The skill depends on the obsidian-cli Homebrew tap.

Mitigation: Confirm that the Homebrew tap is trusted before installing or running obsidian-cli.

## Reference(s):

- [Obsidian Help](https://help.obsidian.md)
- [ClawHub Skill Page](https://clawhub.ai/litiao1224/skills/obsidian-litiao)
- [Publisher Profile](https://clawhub.ai/user/litiao1224)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and file path guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local Obsidian vault paths and obsidian-cli commands; users should confirm vault and note paths before destructive operations.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
