## Description:

Convert PDF to editable Word and automatically verify the conversion quality. Runs a four-way reconciliation (character count, table count, image count, table-cell count) plus a page-count reference after conversion, so content loss or redundancy is surfaced as evidence instead of guesswork. Use when the user asks to convert PDF to Word, convert PDF to docx, check conversion quality, verify a converted document, or worries that PDF-to-Word conversion dropped content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiyanjun](https://clawhub.ai/user/xiyanjun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing users use this skill to convert PDFs into editable Word documents and review whether conversion lost or added content. It is useful when conversion quality, scanned PDF OCR, table preservation, image preservation, or batch PDF-to-DOCX review matters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that the skill recommends installing converter code from an unpinned live GitHub source, so code executed later can differ from the reviewed version.

Mitigation: Prefer a pinned and reviewed PyPI version or immutable Git commit, run in a virtual environment or sandbox, and avoid administrator or root execution.

Risk: PDF content is processed by an external converter, which can expose confidential document contents to local tools and generated reports.

Mitigation: Process sensitive PDFs only in an approved local environment and review output DOCX, JSON, and HTML report paths before sharing.

Risk: OCR and layout polish have platform-dependent behavior; missing OCR dependencies or non-macOS layout polish limitations can affect scanned-PDF results.

Mitigation: Install the appropriate OCR backend for scanned PDFs, use no-polish mode where required, and manually review low-confidence OCR blocks or flagged reconciliation differences.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiyanjun/skills/pdf2word-review)
- [Publisher profile](https://clawhub.ai/user/xiyanjun)
- [PyPI project: pdf2word-review](https://pypi.org/project/pdf2word-review/)
- [Engine repository: pdf-to-word-review](https://github.com/xiyanjun/pdf-to-word-review)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and conversion-quality review tables; may produce DOCX, JSON, and HTML report file paths for the user.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides an agent to run a PDF-to-DOCX converter, request verification reports, and explain character, table, image, table-cell, and OCR confidence differences in plain language.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
