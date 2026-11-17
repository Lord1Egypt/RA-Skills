## Description:

Work with Obsidian vaults (plain Markdown notes) and automate via obsidian-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michael-c-matias](https://clawhub.ai/user/michael-c-matias)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to help agents locate Obsidian vaults, search note names and contents, create notes, move or rename notes while preserving links, and delete notes through obsidian-cli.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Homebrew installation uses a third-party tap for obsidian-cli.

Mitigation: Verify that the publisher and tap are trusted before installing, and consider whether the official Obsidian CLI better fits the environment.

Risk: The delete command can remove note data from an Obsidian vault.

Mitigation: Check the target note or path before running delete, and prefer reviewable direct file edits when appropriate.

Risk: Creating or moving notes in the wrong vault can affect personal or work notes unintentionally.

Mitigation: Use obsidian-cli print-default or Obsidian's local vault configuration to confirm the active vault before running write operations.

## Reference(s):

- [Obsidian Help](https://help.obsidian.md)
- [ClawHub Skill Page](https://clawhub.ai/michael-c-matias/skills/obsidian-cli-notesmd)
- [Publisher Profile](https://clawhub.ai/user/michael-c-matias)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires obsidian-cli and an Obsidian desktop vault configuration; commands operate on local Markdown notes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
