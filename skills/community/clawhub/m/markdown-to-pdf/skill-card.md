## Description:

Convert Markdown files to beautiful PDF documents. Supports custom styling, code highlighting, and multiple output options. Use when users need to convert MD to PDF for documentation, notes, reports, or sharing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alone86136](https://clawhub.ai/user/alone86136)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and documentation authors use this skill to convert Markdown notes, reports, and documentation into shareable PDF files with optional custom styling and code highlighting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The converter gives the PDF renderer broad local file access while processing Markdown, and embedded HTML or resource links may reach local files or network resources available to the user account.

Mitigation: Convert only trusted Markdown, or run the converter in a restricted environment with limited filesystem and network access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alone86136/skills/markdown-to-pdf)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions]

**Output Format:** [PDF file generated from Markdown, with Markdown usage guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the markdown and pygments Python packages plus the wkhtmltopdf system binary; custom CSS can be supplied.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
