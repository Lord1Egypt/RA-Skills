## Description:

Work with Obsidian vaults (plain Markdown notes) and automate via obsidian-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nidhov01](https://clawhub.ai/user/nidhov01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to locate Obsidian vaults, inspect Markdown notes, and run obsidian-cli workflows for search, creation, move, rename, and delete operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing obsidian-cli through the yakitrak/yakitrak Homebrew tap requires trusting a third-party CLI distribution path.

Mitigation: Install only if comfortable trusting that Homebrew tap and review the installed tool before using it on important vaults.

Risk: Create, move, rename, and delete operations can modify or remove Obsidian notes.

Mitigation: Confirm the selected vault and note path before running mutating commands, and keep recoverable backups of important vaults.

Risk: Multiple Obsidian vaults can make it easy to act on the wrong folder.

Mitigation: Use obsidian-cli print-default or Obsidian's vault config to confirm the active vault instead of guessing or hardcoding paths.

## Reference(s):

- [Obsidian Help](https://help.obsidian.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with inline shell commands and note-path examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides the agent to confirm the active vault before mutating notes.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
