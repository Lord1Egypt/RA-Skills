## Description: <br>
Extract text from images using Tesseract.js OCR locally without an API key, with support for Simplified Chinese, Traditional Chinese, and English. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaw555](https://clawhub.ai/user/shaw555) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run local OCR over image files and return extracted text or structured OCR details without configuring an external OCR API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: First use may download Tesseract language data, which can be unsuitable for restricted or offline environments. <br>
Mitigation: Preload or vendor required language data through a controlled process before deployment in restricted environments. <br>
Risk: Sensitive image content may become visible as extracted text in the agent session. <br>
Mitigation: Avoid OCRing sensitive images unless the session and downstream handling are approved for that data. <br>
Risk: The skill depends on npm packages for OCR execution. <br>
Mitigation: Install from a trusted registry and review dependency provenance before use in managed environments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shaw555/ocr-local) <br>
- [Tesseract.js](https://github.com/naptha/tesseract.js) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands] <br>
**Output Format:** [Plain text or JSON OCR results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [JSON output includes recognized text, confidence, words, and bounding boxes when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
