## Description: <br>
Parse documents using PaddleOCR's API. Supports both sync and async modes for images and PDFs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hioTEC](https://clawhub.ai/user/hioTEC) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and document-processing teams use this skill to send selected images or PDFs to a configured PaddleOCR endpoint and receive structured OCR results, including Markdown text and layout parsing data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents are uploaded to the configured PaddleOCR API endpoint for OCR processing. <br>
Mitigation: Use only trusted HTTPS values for PADDLEOCR_API_URL and PADDLEOCR_JOB_URL, and avoid confidential or regulated documents unless external processing is approved. <br>
Risk: The skill requires a PaddleOCR access token for API calls. <br>
Mitigation: Use a scoped, revocable token and rotate it if endpoint trust or local environment security is uncertain. <br>


## Reference(s): <br>
- [PaddleOCR Official Website](https://www.paddleocr.com) <br>
- [PaddleOCR API Documentation](https://ai.baidu.com/ai-doc/AISTUDIO/Cmkz2m0ma) <br>
- [PaddleOCR GitHub](https://github.com/PaddlePaddle/PaddleOCR) <br>
- [PaddleOCR Quota Information](https://ai.baidu.com/ai-doc/AISTUDIO/Xmjclapam) <br>
- [ClawHub Skill Page](https://clawhub.ai/hioTEC/paddleocr-doc-parsing-v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON responses containing structured OCR results and Markdown document text, with shell command examples and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-configured PaddleOCR API credentials and endpoint URLs.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
