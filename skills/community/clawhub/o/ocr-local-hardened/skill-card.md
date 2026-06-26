## Description: <br>
Extract text from images using Tesseract.js OCR (100% local, no API key required). Supports Chinese (simplified/traditional) and English. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and agents use this skill to extract OCR text from local image files, including Chinese and English screenshots or documents, without an external OCR API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OCR output can contain credentials, private messages, or other sensitive text from screenshots and documents. <br>
Mitigation: Review and redact OCR output before sharing it, and keep extracted text on the local machine unless the user explicitly approves a safe destination. <br>
Risk: The skill depends on a Node.js OCR helper, the tesseract.js npm package, and first-run language data downloads unless already cached. <br>
Mitigation: Install only in environments where npm dependencies and language data downloads are acceptable, and review dependency sources before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/ocr-local-hardened) <br>
- [Tesseract.js](https://github.com/naptha/tesseract.js) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands] <br>
**Output Format:** [Plain text or JSON emitted by a local Node CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [JSON output includes recognized text, confidence, words, and word bounding boxes; supported language codes include chi_sim, chi_tra, and eng.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
