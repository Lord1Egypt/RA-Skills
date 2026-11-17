## Description:

Work with Obsidian vaults (plain Markdown notes) and automate via obsidian-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohdalhashemi98-hue](https://clawhub.ai/user/mohdalhashemi98-hue)

### License/Terms of Use:


## Use Case:

Developers, writers, and other Obsidian users use this skill to locate active vaults, search Markdown notes, and run obsidian-cli commands for creating, moving, renaming, deleting, or directly editing notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Create, move, direct edit, and delete commands make real changes to an Obsidian vault.

Mitigation: Confirm the target vault and note path before destructive actions, and rely on backups, sync history, or version control for recovery.

Risk: The skill depends on the obsidian-cli Homebrew tap and local Obsidian vault configuration.

Mitigation: Install only if you trust the obsidian-cli tap, verify obsidian-cli is available, and use the active vault configuration instead of hardcoded vault paths.

## Reference(s):

- [Obsidian Help](https://help.obsidian.md)
- [ClawHub skill page](https://clawhub.ai/mohdalhashemi98-hue/skills/mh-obsidian)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and note-management guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires obsidian-cli and, for URI-based note creation, a working Obsidian URI handler.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
