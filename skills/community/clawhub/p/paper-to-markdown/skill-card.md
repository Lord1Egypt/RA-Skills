## Description:

PDF to Markdown converter - extract text, tables and formulas from PDF files to clean Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanis90](https://clawhub.ai/user/tanis90)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and document-analysis users use this skill to convert local PDF files or PDF URLs into Markdown for extraction, summarization, and downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected PDFs or PDF URLs are sent to MinerU's online service for conversion.

Mitigation: Require explicit user confirmation before processing sensitive, private, regulated, or client documents.

Risk: The skill depends on installing and executing the external mineru-open-api CLI.

Mitigation: Prefer pinned or sandboxed CLI installation where possible and verify the installed binary source before use.

Risk: Markdown-only extraction can replace images, tables, or formulas with placeholders.

Mitigation: Review converted output before relying on it for precise technical, legal, financial, or research analysis.

## Reference(s):

- [Paper To Markdown ClawHub Release](https://clawhub.ai/tanis90/skills/paper-to-markdown)
- [MinerU Homepage](https://mineru.net)
- [MinerU GitHub Project](https://github.com/opendatalab/MinerU)
- [MinerU CLI Download](https://mineru.net/ecosystem?tab=cli)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Markdown-only extraction output; images, tables, and formulas may be represented with placeholders.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
