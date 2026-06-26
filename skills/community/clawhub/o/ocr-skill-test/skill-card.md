## Description: <br>
Extract text from images using Tesseract.js OCR with support for Simplified Chinese, Traditional Chinese, and English. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaw555](https://clawhub.ai/user/shaw555) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run local OCR on screenshots, documents, and other image files, returning recognized text or structured JSON with confidence details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs an npm dependency and may download OCR language data on first use. <br>
Mitigation: Review the dependency before deployment and allow first-run language-data downloads only in environments where that network and cache behavior is acceptable. <br>
Risk: The skill processes user-selected local image files, which may contain sensitive information. <br>
Mitigation: Run OCR only on images whose contents are appropriate to process locally and store according to the user's data-handling requirements. <br>
Risk: OCR quality can vary, especially for handwritten, low-contrast, or poorly lit images. <br>
Mitigation: Review extracted text before relying on it, and prefer clear, high-contrast input images for higher accuracy. <br>


## Reference(s): <br>
- [Tesseract.js](https://github.com/naptha/tesseract.js) <br>
- [ClawHub Skill Page](https://clawhub.ai/shaw555/ocr-skill-test) <br>
- [Publisher Profile](https://clawhub.ai/user/shaw555) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands] <br>
**Output Format:** [Plain text or JSON emitted by a local Node.js OCR command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [JSON output includes recognized text, confidence, word-level confidence, and bounding boxes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
