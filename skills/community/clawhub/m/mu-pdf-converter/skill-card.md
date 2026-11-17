## Description:

Converts valid, text-layer PDF files into editable PowerPoint, Word, Excel, image, filled-form, or watermark-removed outputs while preserving layout where possible.

This skill is ready for commercial/non-commercial use.

## Publisher:

[muippt](https://clawhub.ai/user/muippt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and office automation users use this skill to convert valid PDF documents into editable office files, images, extracted tables, completed forms, or cleaned PDFs. It is not intended for non-PDF inputs, document summarization, or OCR of scanned PDFs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF-to-PPT translation may send document text to external or configured translation or LLM endpoints without clear user consent.

Mitigation: Use --no-translate for confidential PDFs unless translation is explicitly requested and the configured endpoint has been reviewed.

Risk: Generated spreadsheets from untrusted PDFs may expose users to formula injection until the output is fixed or checked.

Mitigation: Inspect or sanitize generated spreadsheets before opening them, especially when the input PDF is untrusted.

Risk: Dependency behavior can vary because the skill documentation recommends installing several packages without pinned versions.

Mitigation: Install the skill in a dedicated virtual environment and pin dependency versions before operational use.

Risk: Watermark removal changes document content and may be inappropriate for protected or policy-controlled documents.

Mitigation: Use watermark removal only for documents the user is authorized to modify, and retain the original file.

## Reference(s):

- [Usage Guide](references/usage-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/muippt/skills/mu-pdf-converter)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands and generated document or image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces office documents, images, PDFs, or extraction outputs depending on the selected converter script.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
