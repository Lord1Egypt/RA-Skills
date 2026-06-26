## Description: <br>
Extract text from images using Tesseract.js OCR (100% local, no API key required). Supports Chinese (simplified/traditional) and English. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nvoicejacob](https://clawhub.ai/user/nvoicejacob) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to extract text from local image files, including Simplified Chinese, Traditional Chinese, and English content. It is suited for local OCR workflows that need plain text or structured JSON output without an API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The first OCR run may download Tesseract language data, which can be unsuitable for offline or tightly controlled environments. <br>
Mitigation: Pre-provision the needed language data and install dependencies from the included lockfile or with exact pins before use. <br>
Risk: OCR accuracy can vary on unclear, low-contrast, poorly lit, or handwritten images. <br>
Mitigation: Use clear, high-contrast source images and review extracted text before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nvoicejacob/ocr-local-1-0-0) <br>
- [Tesseract.js](https://github.com/naptha/tesseract.js) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON emitted by a local Node.js OCR command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [JSON output includes recognized text, overall confidence, word-level confidence, and bounding boxes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
