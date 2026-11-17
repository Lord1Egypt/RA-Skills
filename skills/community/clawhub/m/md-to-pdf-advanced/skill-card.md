## Description:

Convert Markdown files to PDF with multiple backend options (WeasyPrint, Pandoc, wkhtmltopdf), including syntax highlighting, tables, images, custom CSS themes, and page styling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[20181112523](https://clawhub.ai/user/20181112523)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document authors use this skill to convert Markdown files into styled PDF documents for reports, papers, and generated documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change the Python environment when dependencies are missing.

Mitigation: Run it in an isolated virtual environment or container and preinstall pinned dependencies before use.

Risk: Markdown, CSS, or rendered document resources can be controlled by the input document.

Mitigation: Avoid untrusted Markdown or CSS unless local file access and outbound network access are sandboxed.

Risk: The conversion writes PDF output to a specified filesystem path.

Mitigation: Use a dedicated output directory with least-privilege permissions and review output paths before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/20181112523/skills/md-to-pdf-advanced)
- [Publisher profile](https://clawhub.ai/user/20181112523)
- [Bundled skill definition](artifact/SKILL.md)
- [Conversion script](artifact/scripts/md_to_pdf.py)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell and Python command examples; the bundled script writes PDF files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write PDF output to a user-specified path and may use local CSS themes or optional conversion backends.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
