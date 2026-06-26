## Description: <br>
Extract text from images using Tesseract.js OCR (100% local, no API key required). Supports Chinese (simplified/traditional) and English. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[15914355527](https://clawhub.ai/user/15914355527) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to extract Chinese or English text from screenshots, documents, and image files locally without an API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: npm installation and first OCR use may fetch tesseract.js or Tesseract language data from the network. <br>
Mitigation: For locked-down or offline environments, pre-vendor or pre-cache the npm dependency and required language files before use. <br>
Risk: OCR may expose sensitive text from processed images inside the local agent session. <br>
Mitigation: Use the skill only on images whose extracted text is appropriate to reveal in the local agent context. <br>
Risk: OCR accuracy can vary on unclear, low-contrast, poorly lit, or handwritten images. <br>
Mitigation: Review extracted text before relying on it and prefer clear, high-contrast source images. <br>


## Reference(s): <br>
- [Tesseract.js](https://github.com/naptha/tesseract.js) <br>
- [ClawHub skill page](https://clawhub.ai/15914355527/ocr-local-v2) <br>
- [Publisher profile](https://clawhub.ai/user/15914355527) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON emitted by a local Node.js OCR command.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [JSON output includes extracted text, confidence scores, words, and word bounding boxes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
