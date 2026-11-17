## Description:

Syncs Markdown files from a chosen local folder into a specified Obsidian Vault subdirectory while preserving the source directory structure and excluding common development and cache folders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soroyue](https://clawhub.ai/user/soroyue)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agent users, and Obsidian users use this skill to copy Markdown notes, skill files, memory folders, or project documentation from a local source directory into an Obsidian Vault. It is intended for one-way folder synchronization when the user provides a source path, Vault path, and optional target subdirectory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can copy Markdown from arbitrary local folders, including agent skills or memory, into an Obsidian Vault.

Mitigation: Manually verify the source path and Vault path before running it, and avoid syncing folders that may contain secrets or sensitive notes.

Risk: Destination subdirectory handling can write outside the intended Vault if an untrusted destination name is used.

Mitigation: Use only trusted, simple destination subdirectory names and inspect the resolved target path until path traversal handling is hardened.

Risk: The release security verdict is suspicious because path and temporary-directory handling require review.

Mitigation: Review the script before installation and run it only in a trusted local environment with known source and destination paths.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and local shell output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a source directory, an Obsidian Vault path, and an optional Vault subdirectory; execution can copy Markdown files on the local filesystem.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
