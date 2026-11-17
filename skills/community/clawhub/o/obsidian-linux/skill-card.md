## Description:

Work with Obsidian vaults (plain Markdown notes) and automate via notesmd-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tripleight](https://clawhub.ai/user/tripleight)

### License/Terms of Use:


## Use Case:

Developers and Obsidian users use this skill to locate vaults, search and read Markdown notes, create or append daily notes, and manage note paths through notesmd-cli.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required notesmd-cli package is installed from third-party Homebrew or AUR packaging sources.

Mitigation: Verify that the notesmd-cli tap or AUR package is trusted before installation.

Risk: Overwrite, move, or delete commands can modify local Obsidian vault notes, including sensitive or work data.

Mitigation: Confirm the active vault and exact note path before running destructive commands.

## Reference(s):

- [Obsidian Help](https://help.obsidian.md)
- [ClawHub skill page](https://clawhub.ai/tripleight/skills/obsidian-linux)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Obsidian vault access and notesmd-cli.]

## Skill Version(s):

1.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
