## Description: <br>
ifly-pdf&image-ocr supports image OCR and PDF document recognition using iFlytek OCR APIs, including text extraction, PDF conversion, layout-aware recognition, and JSON or Markdown output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qingzhe2020](https://clawhub.ai/user/qingzhe2020) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to extract text from images and PDFs, convert PDFs to Word, Markdown, or JSON, and retrieve structured OCR results through iFlytek services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images and PDFs are sent to iFlytek's remote OCR service. <br>
Mitigation: Use the skill only for documents approved for third-party processing, and use dedicated iFlytek credentials where possible. <br>
Risk: PDF processing may return download URLs or write OCR output to a requested path. <br>
Mitigation: Review returned URLs and saved output locations before sharing or using generated files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qingzhe2020/ifly-pdf-image-ocr) <br>
- [iFlytek Open Platform](https://console.xfyun.cn/) <br>
- [iFlytek OCR service page](https://console.xfyun.cn/services/se75ocrbm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [CLI output, saved text files, Markdown, JSON, and Word document download URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires iFlytek credentials. PDF jobs may return task IDs, page-level results, and temporary download URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
