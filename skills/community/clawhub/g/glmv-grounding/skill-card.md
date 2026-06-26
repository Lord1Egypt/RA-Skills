## Description: <br>
A skill that uses GLM-V native grounding capabilities for coordinate conversion, bounding-box visualization, image target grounding, and video target tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaredforreal](https://clawhub.ai/user/jaredforreal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to ground prompt-described targets in images or videos with GLM-V, then extract normalized coordinates and optionally produce annotated visualizations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected images, videos, and prompts to the external Zhipu GLM-V service. <br>
Mitigation: Use it only when that external processing is acceptable, and avoid media or prompts that contain sensitive information. <br>
Risk: The skill requires a ZHIPU_API_KEY credential and can create a local .env file for configuration. <br>
Mitigation: Use a dedicated revocable API key and keep generated .env files out of version control. <br>
Risk: The skill installs and runs Python dependencies for media processing and visualization. <br>
Mitigation: Install dependencies in an isolated environment before using the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jaredforreal/glmv-grounding) <br>
- [GLM-V grounding source homepage](https://github.com/zai-org/GLM-V/tree/main/skills/glmv-grounding) <br>
- [Zhipu API key setup](https://www.bigmodel.cn/usercenter/proj-mgmt/apikeys) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, files] <br>
**Output Format:** [Markdown or JSON-like coordinate data with optional image or video visualization files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Grounding coordinates are normalized to a 0-1000 image coordinate range; visualizations may be written to a user-selected directory.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
