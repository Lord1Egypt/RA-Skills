## Description: <br>
Extract text content from images using Tesseract OCR via Python. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to extract machine-readable text from JPG, PNG, WEBP, screenshots, scanned documents, receipts, forms, and other images with visible text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security verdict is suspicious because the release evidence reports broad administrative and full-access review capabilities. <br>
Mitigation: Install only in a trusted maintainer workspace, consider disabling full-access autoreview with `--no-yolo` or `AUTOREVIEW_YOLO=0`, and use least-privilege credentials with explicit confirmation for privileged commands. <br>
Risk: OCR output can be incomplete or inaccurate for low-resolution images, handwriting, complex layouts, redactions, watermarks, decorative fonts, or degraded source images. <br>
Mitigation: Use clear images, preprocess when needed, choose appropriate Tesseract page-segmentation settings, preserve warnings, and review extracted text before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wu-uk/jpg-ocr-stat-image-ocr) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, code, guidance] <br>
**Output Format:** [JSON OCR results with optional Markdown guidance and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes extracted text, confidence, detected metadata, and warnings about OCR quality or failures.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
