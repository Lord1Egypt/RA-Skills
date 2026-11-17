## Description:

Obsidian Manager helps agents create and search local Obsidian Markdown notes, while preserving compatibility for workflows that have moved to the knowledge entry point.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jirboy](https://clawhub.ai/user/jirboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to let an agent manage a local Obsidian research vault by creating templated notes and searching Markdown note content. It is also a compatibility layer for older obsidian commands after migration to the knowledge obsidian workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scripts can read or write Markdown files outside the intended research vault if path inputs are not constrained.

Mitigation: Use only a trusted local Obsidian vault, avoid absolute paths and '..' in title or direction arguments, and prefer an allowlist of vault subdirectories before execution.

Risk: Local note creation may overwrite an existing Markdown note when a user confirms the overwrite prompt.

Mitigation: Review the target note path before confirming overwrite prompts and keep backups or version control for the vault.

## Reference(s):

- [Obsidian Manager on ClawHub](https://clawhub.ai/jirboy/skills/obsidian-manager)
- [Publisher profile: jirboy](https://clawhub.ai/user/jirboy)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown and plain text with optional JSON search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or read local Markdown files in an Obsidian research vault.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
