## Description: <br>
Extract text from images via the PDFAPIHub cloud OCR API, with optional preprocessing and word-level bounding boxes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rishabhdugar](https://clawhub.ai/user/rishabhdugar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to extract OCR text from receipts, signs, documents, business cards, labels, and other images through PDFAPIHub's hosted OCR service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images and OCR results are sent to PDFAPIHub for processing. <br>
Mitigation: Avoid highly sensitive images unless the provider's privacy and retention practices are acceptable for the use case. <br>
Risk: The skill requires a PDFAPIHub API key. <br>
Mitigation: Use a dedicated API key that can be rotated and avoid exposing it in prompts, logs, or shared examples. <br>


## Reference(s): <br>
- [PDFAPIHub](https://pdfapihub.com) <br>
- [PDFAPIHub Documentation](https://pdfapihub.com/docs) <br>
- [Image OCR Parse ClawHub Release](https://clawhub.ai/rishabhdugar/image-ocr-parse) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, guidance] <br>
**Output Format:** [JSON or text returned from the OCR API, including extracted text and optional word-level bounding boxes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PDFAPIHUB_API_KEY and uploads selected images to PDFAPIHub for OCR processing.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
