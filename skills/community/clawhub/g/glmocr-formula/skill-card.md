## Description: <br>
Recognizes and extracts mathematical formulas from images and PDFs into LaTeX format using the ZhiPu GLM-OCR API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaredforreal](https://clawhub.ai/user/jaredforreal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and document-processing users use this skill to send selected formula images, PDFs, or URLs to ZhiPu GLM-OCR and receive extracted text and mathematical formulas in Markdown or LaTeX. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected local files or remote URLs to ZhiPu's remote OCR service. <br>
Mitigation: Use it only for documents that are approved for processing by that service, and avoid submitting confidential or regulated content unless policy allows it. <br>
Risk: Saved JSON output and files created with --include-raw may contain extracted document text, formulas, metadata, or raw upstream response data. <br>
Mitigation: Store outputs in approved locations, share them only with intended recipients, and enable --include-raw only when needed for debugging. <br>
Risk: A ZHIPU_API_KEY is required to call the service. <br>
Mitigation: Provide the key through the configured environment, rotate it according to local credential policy, and do not paste it into prompts, logs, or saved result files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jaredforreal/glmocr-formula) <br>
- [GLM-OCR Formula homepage](https://github.com/zai-org/GLM-OCR/tree/main/skills/glmocr-formula) <br>
- [ZhiPu Layout Parsing API documentation](https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E6%96%87%E6%A1%A3%E8%A7%A3%E6%9E%90) <br>
- [ZhiPu API key management](https://bigmodel.cn/usercenter/proj-mgmt/apikeys) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance and JSON CLI output containing extracted text, layout details, errors, source metadata, and optional raw API response data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZHIPU_API_KEY; GLM_OCR_TIMEOUT can adjust request timeout; saved output and optional raw responses may contain sensitive document text or metadata.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
