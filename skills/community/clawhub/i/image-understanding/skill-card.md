## Description: <br>
Provides guidance and sample code for integrating ZhipuAI GLM-4.6V vision models for image understanding, document analysis, and multimodal tool-calling workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[IsabellaZhangYM](https://clawhub.ai/user/IsabellaZhangYM) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers use this skill to configure ZhipuAI API credentials, install the SDK, and call GLM-4.6V for OCR, document and presentation understanding, UI screenshot analysis, and structured visual extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image, document, screenshot, or business content submitted to the vision model may include sensitive information. <br>
Mitigation: Redact sensitive IDs, financial records, private screenshots, and confidential business content before sending inputs to the provider. <br>
Risk: The skill depends on an external ZhipuAI SDK and API key for model calls. <br>
Mitigation: Install the SDK from a verified package source and keep the API key in the ZHIPUAI_API_KEY environment variable instead of hard-coding credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/IsabellaZhangYM/image-understanding) <br>
- [ZhipuAI API documentation](https://open.bigmodel.cn/) <br>
- [ZhipuAI Vision MCP documentation](https://docs.bigmodel.cn/cn/coding-plan/mcp/vision-mcp-server) <br>
- [GLM-V repository](https://github.com/zai-org/GLM-V) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a ZHIPUAI_API_KEY environment variable and sends selected images or documents to ZhipuAI services.] <br>

## Skill Version(s): <br>
0.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
