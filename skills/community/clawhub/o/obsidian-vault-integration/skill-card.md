## Description:

Read and write data with an Obsidian vault used as a shared knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dmanock](https://clawhub.ai/user/dmanock)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to treat an Obsidian vault as a shared knowledge base for reading notes, extracting structured task and team data, and writing updates back to vault Markdown files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File handling can escape the configured vault and read or modify other local files.

Mitigation: Install only after review, use with a trusted non-sensitive vault, prevent untrusted prompts or note content from choosing filenames, and require explicit approval before write actions.

## Reference(s):

- [File Format Reference](references/file-formats.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and JSON output from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads and writes local Obsidian Markdown files using a configured vault path.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
