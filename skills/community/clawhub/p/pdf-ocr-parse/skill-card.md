## Description:

Extract text from scanned PDFs using Tesseract OCR. Supports multiple languages, page selection, DPI control, and word-level bounding boxes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rishabhdugar](https://clawhub.ai/user/rishabhdugar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to OCR scanned PDFs such as invoices, forms, legacy records, insurance claims, and legal documents into searchable text and optional word-level data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDFs, document URLs, and OCR results are sent to pdfapihub.com for processing.

Mitigation: Use the skill only with documents approved for that third-party service and review the provider's privacy, retention, and contractual terms before sending sensitive data.

Risk: OCR output can be incomplete or inaccurate, especially for low-quality scans, unusual layouts, or multilingual documents.

Mitigation: Use confidence scores and human review before relying on extracted text for accounting, legal, insurance, or other consequential workflows.

## Reference(s):

- [PDF API Hub Documentation](https://pdfapihub.com/docs)
- [PDF OCR Parse on ClawHub](https://clawhub.ai/rishabhdugar/skills/pdf-ocr-parse)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON or plain text containing OCR text, confidence scores, and optional word-level bounding boxes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include full_text, per-page text, character counts, language, processed page counts, and word bounding boxes when detail is words.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
