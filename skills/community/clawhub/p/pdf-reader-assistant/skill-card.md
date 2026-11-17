## Description:

PDF阅读助手 helps agents extract and analyze PDF text, tables, OCR content, summaries, keywords, image locations, and comparisons across one or more PDF files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guipi888](https://clawhub.ai/user/guipi888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to inspect local PDF files, extract text and tables, OCR scanned documents, create structured reading reports, compare multiple PDFs, and batch summarize PDF folders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Extracted PDF contents may be written to the predictable temporary path /tmp/pdf_extract.json when following the documented workflow.

Mitigation: Use a private temporary path or in-memory flow for sensitive documents, delete generated outputs after use, and process only documents acceptable for local script handling.

Risk: Optional PDF, table, and OCR dependencies can affect runtime behavior and supply-chain exposure if installed ad hoc.

Mitigation: Install dependencies in an isolated virtual environment with pinned versions before using the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guipi888/skills/pdf-reader-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON extraction results, shell commands, and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include extracted document text, table Markdown, metadata, OCR status, page-level image counts, keywords, and comparison summaries.]

## Skill Version(s):

2.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
