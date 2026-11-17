## Description:

Automatically clean up loose images and attachments in an Obsidian vault root by moving them into an Attachments folder.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sparkingskin-tech](https://clawhub.ai/user/sparkingskin-tech)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to organize loose files in an Obsidian vault root into an attachments folder, with a dry-run mode to preview file moves before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move local files beyond ordinary attachment cleanup, including Obsidian notes and text files.

Mitigation: Run it only on a backed-up vault, use --dry-run first, and require explicit opt-in before moving .md or .txt files.

Risk: A custom attachments path could move files outside the selected vault if broad paths are accepted.

Mitigation: Avoid absolute or parent-traversal attachments paths and confine the destination inside the selected vault.

Risk: Broad trigger-based execution may move files when the user did not intend to perform cleanup.

Mitigation: Require clear user confirmation before running non-dry-run cleanup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sparkingskin-tech/skills/obsidian-cleaner)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance]

**Output Format:** [Markdown with inline bash commands and text reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local file-move guidance and status output; dry-run mode can preview changes before files are moved.]

## Skill Version(s):

1.0.0 (source: release evidence, _meta.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
