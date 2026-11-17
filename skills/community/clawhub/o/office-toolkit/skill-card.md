## Description:

A comprehensive toolkit for Microsoft Office documents (Word, Excel, PowerPoint) and PDF files that supports reading, writing, format conversion, and batch processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weiwei2027](https://clawhub.ai/user/weiwei2027)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to inspect, create, and convert Office and PDF documents through Python-backed command-line tools. It is suited for document extraction, simple document generation, and workflow automation around DOCX, PPTX, XLSX, and PDF files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The document scripts read input files and write output files on disk, so careless paths can overwrite or create files in unintended locations.

Mitigation: Run the tools in a controlled working directory and review output paths before execution.

Risk: Processing untrusted Office, PDF, or spreadsheet data can expose the workflow to malformed files or formula-like spreadsheet values.

Mitigation: Use trusted documents when possible, pin and audit dependencies, and escape formula-like values before writing XLSX data unless formulas are explicitly intended.

Risk: DOCX-to-PDF and PPTX-to-PDF conversion depends on optional packages or external office software and may fail when those tools are unavailable.

Mitigation: Install and verify required conversion dependencies before relying on PDF conversion in production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weiwei2027/skills/office-toolkit)
- [Artifact README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands; scripts emit plain text, JSON, or document files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and optional Python packages for DOCX, PPTX, XLSX, and PDF operations.]

## Skill Version(s):

1.0.1 (source: frontmatter, server release metadata, target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
