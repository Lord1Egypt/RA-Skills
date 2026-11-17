## Description:

Convert Kindle HTML notebook exports to Obsidian Markdown format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[henrch1](https://clawhub.ai/user/henrch1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert Kindle notebook HTML exports into Obsidian-ready Markdown notes, with the output path configured in the skill reference file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow uses an unsafe shell command pattern when invoking the local converter.

Mitigation: Review the command before execution, use structured argument passing where possible, and avoid converting HTML files from untrusted sources.

Risk: The runtime overwrites existing Markdown notes by default.

Mitigation: Confirm the configured output directory and generated filename before running, and keep backups or remove override behavior when preserving existing notes matters.

Risk: The converter reads local Kindle HTML exports and writes into the user's Obsidian folder.

Mitigation: Install only when comfortable with that local file access, and review the configured output path before first use.

## Reference(s):

- [Configuration reference](references/config.md)
- [ClawHub skill page](https://clawhub.ai/henrch1/skills/kindle2md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown file plus concise status or error text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a Markdown note to the configured Obsidian output directory and may overwrite an existing file when run with override behavior.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
