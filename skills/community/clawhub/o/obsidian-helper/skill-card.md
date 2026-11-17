## Description:

Obsidian Helper helps agents operate Obsidian vaults from the command line, including listing, searching, creating, reading, editing, deleting, and daily-note workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[547895019](https://clawhub.ai/user/547895019)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and note-taking users use this skill to have an agent manage local Obsidian Markdown notes through command-line operations such as listing, searching, creating, reading, editing, deleting, and daily notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer modifies the user's shell profile.

Mitigation: Review the install script before running it and confirm PATH changes in the shell profile.

Risk: The artifact does not include the obsidian command script referenced by the installer.

Mitigation: Confirm the missing command script is supplied before relying on the installed command.

Risk: Edit and delete operations can change or remove Obsidian vault files.

Mitigation: Set OBSIDIAN_VAULT explicitly and use backups or version control before running edit or delete workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/547895019/skills/obsidian-helper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown notes, command-line text, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local Obsidian command and OBSIDIAN_VAULT; operations can modify or delete vault files.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
