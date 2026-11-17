## Description:

Work with Obsidian vaults (plain Markdown notes) and automate via obsidian-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonydesign1999](https://clawhub.ai/user/tonydesign1999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to help an agent find Obsidian vaults, search notes, create notes, move or rename notes, delete notes, and edit Markdown files directly when appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to read and modify notes in an Obsidian vault, including move and delete operations.

Mitigation: Confirm the vault and note path before move or delete requests, and keep backups or version history enabled for important notes.

Risk: The skill depends on installing and trusting the third-party obsidian-cli Homebrew tap.

Mitigation: Install only after reviewing and trusting the obsidian-cli Homebrew tap and local environment requirements.

## Reference(s):

- [Obsidian Help](https://help.obsidian.md)
- [ClawHub skill page](https://clawhub.ai/tonydesign1999/skills/obsidian-1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and file path guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands that read, create, move, or delete notes in a selected Obsidian vault.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
