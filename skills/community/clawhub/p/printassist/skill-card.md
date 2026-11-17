## Description:

PrintAssist helps agents print PDFs, Office documents, and images from plain-language requests, including layout options, page ranges, PDF transforms, and optional Adobe Creative Cloud photo editing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nilsgollub](https://clawhub.ai/user/nilsgollub)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and operators use PrintAssist to turn plain-language requests into local Windows print jobs and document preparation steps for PDFs, Office files, and images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive or incorrect documents could be printed directly to a physical or shared printer.

Mitigation: Use preview or explicit confirmation for sensitive, layout-heavy, or shared-printer jobs before execution.

Risk: The setup flow installs third-party Windows software and Python packages.

Mitigation: Run setup only in a trusted Windows environment, and prefer a virtual environment or dependency review before installation.

Risk: Document conversion or PDF manipulation can create modified copies with formatting or content errors.

Mitigation: Review generated PDFs or PNG previews before distributing or printing important documents.

Risk: PDF password removal can create unencrypted copies when a user supplies the password.

Mitigation: Only decrypt documents the user is authorized to handle, and store outputs in controlled locations.

## Reference(s):

- [PrintAssist ClawHub listing](https://clawhub.ai/nilsgollub/skills/printassist)
- [PrintAssist project homepage](https://github.com/nilsgollub/PrintAssist)
- [Claude Code](https://claude.ai/code)
- [OpenClaw](https://openclaw.ai/)
- [SumatraPDF](https://www.sumatrapdfreader.org/download-free-pdf-viewer)
- [LibreOffice](https://www.libreoffice.org/download/download/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown responses with inline code and shell commands; scripts may create PDFs, PNG previews, printer configuration files, modified documents, or physical print jobs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Windows-only execution path; printing depends on configured local printers and installed document tools.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata; artifact frontmatter lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
