## Description:

Extract text from image-based or scanned PDFs using Tesseract OCR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bilicen700](https://clawhub.ai/user/bilicen700)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to extract text from scanned or image-only PDF documents in local environments where Tesseract and the required Python packages are installed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Temporary OCR images may expose document content if written to predictable shared paths.

Mitigation: Use in-memory OCR or a private randomized temporary directory, and remove temporary images immediately after processing.

Risk: OCR quality or coverage may be poor when the required Tesseract language packs are missing or the wrong language option is used.

Mitigation: Install the needed language packs before use and set the Tesseract language option to match the document.

Risk: Runtime dependency installation can introduce operational and security uncertainty.

Mitigation: Pre-install Tesseract, language packs, pypdfium2, pytesseract, and Pillow in a least-privileged environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bilicen700/skills/pdf-ocr-extraction)
- [Publisher profile](https://clawhub.ai/user/bilicen700)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [OCR output depends on installed Tesseract language packs and document image quality.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
