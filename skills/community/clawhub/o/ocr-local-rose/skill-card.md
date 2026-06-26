## Description: <br>
Extract text from images using Tesseract.js OCR (100% local, no API key required). Supports Chinese (simplified/traditional) and English. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[roseknife520](https://clawhub.ai/user/roseknife520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to run local OCR on screenshots, scanned documents, and other image files, with selectable Chinese and English language models and optional structured JSON output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads image files selected by the user and returns extracted text into the agent session. <br>
Mitigation: Use it only with images whose contents are appropriate to expose in the current agent session. <br>
Risk: Installation and first use may download npm packages and Tesseract language data. <br>
Mitigation: Review and approve the npm dependency and language-data downloads before using the skill in restricted environments. <br>
Risk: OCR accuracy can vary for low-quality images or handwriting. <br>
Mitigation: Review extracted text before using it for decisions, records, or downstream automation. <br>


## Reference(s): <br>
- [Tesseract.js](https://github.com/naptha/tesseract.js) <br>
- [ClawHub Skill Page](https://clawhub.ai/roseknife520/ocr-local-rose) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON emitted by a local Node.js OCR command, with markdown usage guidance in the skill instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [JSON output includes recognized text, confidence, words, and bounding boxes when --json is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
