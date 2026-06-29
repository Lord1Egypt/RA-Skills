## Description: <br>
Iflytek Pdf Image Ocr supports image and PDF OCR workflows for extracting text, preserving layout where supported, and converting PDF content to Word, Markdown, or JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iflytek.skills](https://clawhub.ai/user/iflytek.skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and document-processing teams use this skill to extract text from images and PDFs, convert PDFs to Word, Markdown, or JSON, and preserve document layout where supported. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local PDFs, images, or document URLs may be sent to iFlytek or another third-party OCR service without a clear privacy disclosure. <br>
Mitigation: Use the skill only with documents approved for third-party OCR processing, and add an explicit confirmation step before processing private or regulated files. <br>
Risk: Sensitive IDs, contracts, medical, financial, credential-containing, or similarly confidential documents may be exposed through OCR uploads or provider-hosted download URLs. <br>
Mitigation: Avoid those document classes unless provider handling terms have been reviewed; prefer a local OCR option for sensitive material. <br>
Risk: PDF OCR results may include provider-hosted download URLs that can remain accessible for a period after processing. <br>
Mitigation: Retrieve needed outputs promptly, avoid sharing download URLs, and handle returned links as sensitive artifacts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iflytek.skills/iflytek-pdf-image-ocr) <br>
- [iFlytek OCR service homepage](https://www.xfyun.cn/services/ocr) <br>
- [iFlytek image OCR API documentation](https://www.xfyun.cn/doc/words/image_word_recognition/API.html) <br>
- [iFlytek PDF OCR service](https://console.xfyun.cn/services/se75ocrbm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [CLI output, JSON, Markdown, and Word/PDF OCR download links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Image OCR can save extracted text to a file; PDF OCR can return task status, page status, and provider-hosted download URLs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
