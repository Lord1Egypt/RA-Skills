## Description:

Work with Obsidian vaults (plain Markdown notes) and automate via obsidian-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[landercortazarromero](https://clawhub.ai/user/landercortazarromero)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and Obsidian users use this skill to discover vaults, search notes, create notes, and safely propose move, rename, or delete operations through obsidian-cli.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires installing obsidian-cli from a third-party Homebrew tap.

Mitigation: Install only when the Homebrew tap is trusted and the required binary is appropriate for the environment.

Risk: Move, rename, and delete commands can alter or remove notes in an Obsidian vault.

Mitigation: Confirm the active vault and exact note path before execution, and keep backups or Obsidian sync/version history enabled.

Risk: Multiple local vaults can cause commands to target the wrong vault if the vault path is guessed.

Mitigation: Use obsidian-cli print-default or Obsidian's vault configuration to resolve the intended vault before acting.

## Reference(s):

- [Obsidian Help](https://help.obsidian.md)
- [Korta Obsidian on ClawHub](https://clawhub.ai/landercortazarromero/skills/korta-obsidian)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local vault paths and obsidian-cli commands that modify Markdown notes when executed.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
