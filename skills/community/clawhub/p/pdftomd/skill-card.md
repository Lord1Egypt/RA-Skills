## Description:

PDF to Markdown converter - extract text, tables and formulas from PDF files to clean Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanis90](https://clawhub.ai/user/tanis90)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to convert local or URL-based PDF documents into Markdown for extraction, parsing, summarization, or analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF contents are sent to MinerU's external API for conversion.

Mitigation: Do not submit confidential or regulated PDFs unless that external processing flow is approved.

Risk: The helper CLI may be installed from unpinned third-party package sources.

Mitigation: Use a trusted installation source and pin or verify the mineru-open-api package before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tanis90/skills/pdftomd)
- [MinerU homepage](https://mineru.net)
- [MinerU CLI ecosystem page](https://mineru.net/ecosystem?tab=cli)
- [MinerU open-source project](https://github.com/opendatalab/MinerU)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses mineru-open-api for PDF conversion; flash extraction is limited to 10MB and 20 pages, and images, tables, or formulas may be represented with placeholders.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
