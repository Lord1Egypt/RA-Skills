## Description:

Extract text, tables, and metadata from PDFs. Auto-detects native text vs scanned image pages and routes to pdfplumber or Tesseract OCR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alex-ht](https://clawhub.ai/user/alex-ht)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to extract text, tables, and document metadata from native-text or scanned PDFs without manually choosing between text extraction and OCR.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF extraction may process sensitive or unauthorized document contents.

Mitigation: Run the skill only on PDFs the user is authorized to process and store extracted outputs in appropriate local paths.

Risk: Installation depends on Python packages and a system Tesseract OCR binary.

Mitigation: Install in a virtual environment, prefer pinned tags or commits for package installs, and use sudo for Tesseract only with trusted package sources.

Risk: Large or untrusted PDFs can consume substantial OCR resources or accidentally overwrite output files.

Mitigation: Use page ranges and reasonable OCR DPI for large inputs, and choose output paths deliberately.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alex-ht/skills/pdf-extraction)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Python 3 downloads](https://www.python.org/downloads/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Plain text, JSON, or Markdown with CLI command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include page-level text/OCR mode markers, extracted tables, document metadata, or analyze-only classification JSON depending on CLI flags.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
