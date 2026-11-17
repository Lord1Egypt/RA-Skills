## Description:

Provides command reference guidance for using Obsidian CLI to manage notes, vaults, frontmatter, search, and shell completions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0x-cryptopriest](https://clawhub.ai/user/0x-cryptopriest)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill as a command reference when working with Obsidian vaults from the command line, including note creation, search, move, deletion, frontmatter edits, daily notes, and shell completion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Obsidian CLI commands such as overwrite, delete, move, and frontmatter edit can modify or remove local notes.

Mitigation: Confirm the target vault and note name before execution, and keep backups or version history for important notes.

Risk: The artifact includes an environment-specific default vault path example.

Mitigation: Resolve and verify the user's actual vault path before proposing or running vault-specific commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0x-cryptopriest/skills/obsidian-cli-skills)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that modify, move, overwrite, or delete local Obsidian notes.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
