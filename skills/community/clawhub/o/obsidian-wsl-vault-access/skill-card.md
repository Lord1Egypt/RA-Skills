## Description:

Work with an Obsidian vault stored on Windows and accessed from WSL to read, search, create, and edit markdown notes through mounted paths such as /mnt/c or /mnt/d.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wufei-png](https://clawhub.ai/user/wufei-png)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and note-taking users use this skill to let an agent operate on a Windows-hosted Obsidian vault from WSL while preserving Obsidian markdown conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Vault notes may contain private personal data that could be exposed during broad searches or review.

Mitigation: Provide the vault path explicitly and review requested broad searches before execution.

Risk: Bulk edits or incorrect vault-root selection could change unintended notes.

Mitigation: Confirm the vault root before broad operations and prefer targeted edits over full-file rewrites.

Risk: Incorrect Windows-to-WSL path translation could direct work to the wrong location.

Mitigation: Verify translated /mnt/<drive> paths before reading, creating, or editing notes.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with optional shell command snippets and note content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or edit markdown files in a user-provided vault path.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
