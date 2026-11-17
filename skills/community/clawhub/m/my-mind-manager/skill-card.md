## Description:

my-mind Manager helps an agent initialize and manage a local Markdown workspace for ideas, article drafts, published writing, creative assets, inbox items, and archives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amateur0x1](https://clawhub.ai/user/amateur0x1)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to have an agent organize a personal writing workspace, capture ideas, draft articles, mark completed writing as published, and sort creative assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad natural-language triggers could load the skill when the user did not intend file management.

Mitigation: Use explicit invocations such as /my-mind-manager or mention my-mind before applying the workflow.

Risk: The workflow can create directories and Markdown files in a local writing workspace.

Mitigation: Confirm the target workspace path and requested structure before creating files or directories.

Risk: The workflow can move creative assets or mark articles as published by moving and renaming files.

Mitigation: Confirm the exact source files, destination paths, and publishing intent before moving or renaming content.

Risk: The workflow may commit repository changes as part of initialization.

Mitigation: Ask for explicit user confirmation before making commits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/amateur0x1/skills/my-mind-manager)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown files, directory structures, shell command snippets, and concise procedural guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, move, rename, archive, or commit local workspace files after user confirmation.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
