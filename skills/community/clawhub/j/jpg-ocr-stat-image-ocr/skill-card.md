## Description:

Extract text content from images using Tesseract OCR via Python.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to extract machine-readable text from scanned documents, screenshots, receipts, forms, photos, and batches of image files. It provides Tesseract/pytesseract guidance for OCR extraction, confidence handling, preprocessing, and JSON result generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image files and extracted OCR text may contain sensitive information such as receipts, forms, screenshots, or scanned documents.

Mitigation: Process only appropriate local images, treat extracted text and saved JSON results as sensitive, and avoid retaining or sharing OCR outputs unless required.

Risk: OCR output can be incomplete or inaccurate for low-quality images, handwriting, complex layouts, or text in languages not configured for Tesseract.

Mitigation: Use confidence scores and warnings, specify the OCR language when needed, apply preprocessing or page segmentation settings, and review extracted text before relying on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wu-uk/skills/jpg-ocr-stat-image-ocr)

## Skill Output:

**Output Type(s):** [Text, JSON, Code, Guidance]

**Output Format:** [Markdown guidance with Python code examples and JSON OCR result schemas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [OCR quality depends on image clarity, language selection, preprocessing, and Tesseract configuration.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
