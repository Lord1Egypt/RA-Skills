## Description:

Extract text from images via the PDFAPIHub cloud OCR API. Images are uploaded to pdfapihub.com for Tesseract OCR processing. Supports preprocessing (grayscale, sharpen, threshold, resize) and word-level bounding boxes. Requires a CLIENT-API-KEY header.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rishabhdugar](https://clawhub.ai/user/rishabhdugar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to extract text, lines, confidence scores, and optional word-level bounding boxes from images such as receipts, business cards, labels, signs, and documents. It can apply basic preprocessing options to improve OCR quality on low-resolution or noisy inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images are uploaded to PDFAPIHub for hosted OCR processing and may contain sensitive content.

Mitigation: Only process images that the user is permitted to share with PDFAPIHub, and avoid IDs, medical records, invoices, screenshots with secrets, or other sensitive images unless the provider's retention and privacy practices are acceptable.

Risk: The skill requires a PDFAPIHub API key.

Mitigation: Provide the API key only through the required PDFAPIHUB_API_KEY credential path and rotate it if exposure is suspected.

## Reference(s):

- [PDFAPIHub Documentation](https://pdfapihub.com/docs)
- [PDFAPIHub API](https://pdfapihub.com/api)
- [Image OCR Parse on ClawHub](https://clawhub.ai/rishabhdugar/skills/image-ocr-parse)
- [rishabhdugar ClawHub Profile](https://clawhub.ai/user/rishabhdugar)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [JSON or plain text response containing extracted OCR text, line data, confidence scores, and optional word-level bounding boxes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a PDFAPIHUB_API_KEY credential and sends selected images to PDFAPIHub for hosted OCR processing.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
