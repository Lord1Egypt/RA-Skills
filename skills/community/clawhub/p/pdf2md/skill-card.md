## Description:

PDF to Markdown converter - extract text, tables and formulas from PDF files to clean Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanis90](https://clawhub.ai/user/tanis90)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and external users use this skill to convert local PDF files or PDF URLs into Markdown for extraction, summarization, parsing, and analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local PDFs may be uploaded to MinerU's external API during conversion.

Mitigation: Avoid confidential, regulated, privileged, or personal documents unless disclosure to the external service is authorized; use a local-only converter for sensitive files.

Risk: The required CLI is installed from mutable third-party package sources.

Mitigation: Pin and review a specific CLI version before use in controlled environments.

## Reference(s):

- [ClawHub Pdf2md Skill Page](https://clawhub.ai/tanis90/skills/pdf2md)
- [MinerU](https://mineru.net)
- [MinerU CLI](https://mineru.net/ecosystem?tab=cli)
- [OpenDataLab MinerU](https://github.com/opendatalab/MinerU)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Markdown output may include placeholders for images, tables, or formulas; quick mode is limited to 10MB and 20 pages per document.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
