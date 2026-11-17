## Description:

Extract text, tables, and metadata from PDFs; analyze, summarize, and search PDF content, including specific pages or page ranges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wancy86](https://clawhub.ai/user/wancy86)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect user-selected PDF documents, extract text and tables, read metadata, summarize document structure, and search for specific content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive PDF text, tables, or metadata may appear in terminal output, JSON files, CI logs, or transcripts.

Mitigation: Run the skill only on PDFs whose extracted contents may be disclosed in the active terminal, logs, files, and agent transcript.

Risk: PDF extraction and summaries can miss or misread content when document layout, tables, or metadata are complex.

Mitigation: Review extracted text, tables, metadata, and summaries against the source PDF before relying on them for consequential decisions.

## Reference(s):

- [PDF Python Libraries Reference](references/pdf-libraries.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or JSON, with Markdown usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include extracted PDF text, tables, metadata, page statistics, previews, and summaries.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
