## Description:

Interact with Obsidian vaults through the Obsidian CLI to read, create, search, and manage notes, tasks, frontmatter properties, and plugin-development workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sadlay](https://clawhub.ai/user/sadlay)

### License/Terms of Use:


## Use Case:

External users and developers use this skill when they want an agent to operate an Obsidian vault from the command line, including note management, vault search, frontmatter updates, and plugin or theme debugging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands that delete, move, or remove frontmatter can change or remove Obsidian notes.

Mitigation: Confirm the target vault, note path, and intended change before running destructive or modifying commands.

Risk: Screenshot, DOM inspection, note printing, and vault search commands can expose private vault content.

Mitigation: Use these commands only when the user has explicitly identified the vault or note content to inspect.

Risk: Plugin evaluation commands run JavaScript inside Obsidian.

Mitigation: Review the code and confirm the plugin-development context before running evaluation commands.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a running Obsidian instance and the Obsidian CLI plugin.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
