## Description: <br>
Extracts text from scanned PDF files and image files using a local RapidOCR engine or an optional SiliconFlow cloud OCR engine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yejinlei](https://clawhub.ai/user/yejinlei) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to extract text from scanned PDFs, screenshots, and document images, including Chinese and English content. It supports local processing by default and optional cloud OCR when higher accuracy is needed and remote processing is approved. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install Python packages during use. <br>
Mitigation: Review before installing, use a locked environment with pinned dependencies, and require confirmation before package installation. <br>
Risk: The optional SiliconFlow OCR path may send document images to a cloud service. <br>
Mitigation: Use local RapidOCR for confidential files, keep OCR_ENGINE=rapid by default, and configure a cloud API key only when remote processing is approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yejinlei/pdf-ocr-skill) <br>
- [SiliconFlow OCR API endpoint](https://api.siliconflow.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or JSON-like OCR result objects, often described in Markdown with Python and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [OCR results include extracted text, page count, and the engine used; examples also show writing extracted text to files.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
