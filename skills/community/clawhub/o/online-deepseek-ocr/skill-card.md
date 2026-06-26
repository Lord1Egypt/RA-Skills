## Description: <br>
Perform cloud-based OCR on PNG, JPG, JPEG, and WEBP images using SiliconFlow's DeepSeek-OCR with automatic image preprocessing for enhanced recognition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qwq2023qwq](https://clawhub.ai/user/qwq2023qwq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to extract text from user-chosen local images or image URLs through a SiliconFlow-compatible DeepSeek-OCR endpoint. It supports preprocessed image input and can return either readable OCR text or structured JSON with usage metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected screenshots, document photos, or image URLs are sent to the configured SiliconFlow-compatible OCR endpoint. <br>
Mitigation: Use the skill only with data approved for that external service, and avoid sending sensitive or regulated images unless the endpoint is approved for that use. <br>
Risk: The OCR API key is stored in config.json and could be exposed if the file is shared or committed. <br>
Mitigation: Use a dedicated limited API key, keep config.json private, and rotate the key if exposure is suspected. <br>
Risk: Python dependencies are specified with minimum versions rather than exact pins. <br>
Mitigation: Install in an isolated environment and pin reviewed dependency versions for production deployments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qwq2023qwq/online-deepseek-ocr) <br>
- [SiliconFlow](https://siliconflow.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON] <br>
**Output Format:** [Plain text OCR output or JSON result object] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [JSON output includes success status, extracted text, engine, model, and API usage metadata when available.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
