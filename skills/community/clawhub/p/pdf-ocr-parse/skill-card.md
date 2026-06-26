## Description: <br>
Extract text from scanned PDFs using Tesseract OCR. Supports multiple languages, page selection, DPI control, and word-level bounding boxes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rishabhdugar](https://clawhub.ai/user/rishabhdugar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to OCR scanned PDFs such as invoices, receipts, legacy documents, forms, claims, and legal discovery files into searchable text with optional confidence scores and word-level bounding boxes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected PDFs, uploaded files, or PDF URLs are sent to pdfapihub.com for OCR processing. <br>
Mitigation: Review the provider's privacy, retention, and security terms before use, and avoid confidential, regulated, or production documents until those terms are acceptable. <br>
Risk: The skill requires a sensitive API key in the CLIENT-API-KEY header. <br>
Mitigation: Use a dedicated API key stored outside prompts and source files, restrict access where possible, and rotate the key if it is exposed. <br>


## Reference(s): <br>
- [PDF API Hub Documentation](https://pdfapihub.com/docs) <br>
- [PDF OCR Parse on ClawHub](https://clawhub.ai/rishabhdugar/pdf-ocr-parse) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API Calls] <br>
**Output Format:** [JSON response or plain text, depending on output_format] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Per-page text, confidence scores, optional word-level bounding boxes, and full_text; requires a CLIENT-API-KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
