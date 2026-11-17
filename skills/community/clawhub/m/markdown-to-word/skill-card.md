## Description:

Convert a Markdown file or raw Markdown string into a polished Word DOCX document.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mutour](https://clawhub.ai/user/mutour)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document authors use this skill to convert Markdown files or raw Markdown strings into Word DOCX reports, proposals, memos, or documentation with built-in or custom reference templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs the local pandoc executable and reads the Markdown, template, metadata, and resource files selected by the user.

Mitigation: Install and use it only in environments where the local pandoc executable is trusted, and review input, template, metadata, and resource paths before conversion.

Risk: The converter creates parent directories and writes DOCX files to the requested output path.

Mitigation: Review the output path before running the command and avoid broad or sensitive destination directories.

## Reference(s):

- [Markdown to Word example](assets/examples/sample.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and parameter guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may create DOCX files at user-selected output paths and can use templates, metadata, resource paths, a table of contents, and numbered sections.]

## Skill Version(s):

0.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
