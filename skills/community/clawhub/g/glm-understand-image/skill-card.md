## Description: <br>
Uses a GLM vision MCP server to help an agent analyze images, screenshots, diagrams, charts, UI differences, and videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Thincher](https://clawhub.ai/user/Thincher) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and other agent users use this skill to configure the GLM vision MCP server and request visual understanding tasks such as OCR, screenshot diagnosis, diagram interpretation, chart analysis, UI comparison, and general image analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill routes selected images, screenshots, URLs, or videos to an external GLM provider for processing. <br>
Mitigation: Use it only for content approved for external processing, and avoid confidential, regulated, or personal images unless that use has been reviewed. <br>
Risk: The artifact describes saving the GLM API key in a plaintext configuration file. <br>
Mitigation: Prefer a secret manager or locked-down environment variable, restrict file permissions, and avoid printing API keys in terminals or logs. <br>
Risk: The workflow installs or invokes MCP packages through npx without a pinned package version. <br>
Mitigation: Pin package versions where possible and install only in environments where the GLM MCP package and its dependencies are trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Thincher/glm-understand-image) <br>
- [GLM vision MCP server documentation](https://docs.bigmodel.cn/cn/coding-plan/mcp/vision-mcp-server) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and MCP call patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may depend on external GLM provider processing of selected images, screenshots, URLs, or videos.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
