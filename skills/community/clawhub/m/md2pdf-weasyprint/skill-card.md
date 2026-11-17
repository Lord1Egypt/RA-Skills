## Description:

Converts Markdown files into polished PDF documents with Chinese text support, code highlighting, tables, links, images, and custom CSS styling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[franklu0819-lang](https://clawhub.ai/user/franklu0819-lang)

### License/Terms of Use:

MIT

## Use Case:

Developers and content authors use this skill to convert Markdown documentation into PDF files with CJK font support and styled tables and code blocks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wrapper can automatically install unpinned Python packages and system fonts when dependencies are missing.

Mitigation: Use a disposable or controlled environment, preinstall reviewed and pinned dependencies, and avoid running the wrapper with elevated privileges.

Risk: Rendering untrusted Markdown may allow local or network resource access during conversion.

Mitigation: Convert trusted Markdown only, or sandbox filesystem and network access before processing untrusted input.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/franklu0819-lang/skills/md2pdf-weasyprint)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [PDF file output with Markdown usage guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 with markdown and weasyprint; the wrapper may install missing Python packages and system fonts.]

## Skill Version(s):

2.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
