## Description: <br>
Analyze images and videos with Zhipu GLM-V models to generate professional prompts for text-to-image and text-to-video tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaredforreal](https://clawhub.ai/user/jaredforreal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative users use this skill to turn reference images or video URLs into complete prompts for image and video generation workflows such as Midjourney, Stable Diffusion, DALL-E, Sora, Runway, Kling, and Pika. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Zhipu API key and uses it to call an external GLM-V API. <br>
Mitigation: Store ZHIPU_API_KEY only in the configured environment or OpenClaw skill configuration, and rotate it if it may have been exposed. <br>
Risk: Selected images or video URLs are sent to Zhipu for analysis. <br>
Mitigation: Avoid private or sensitive media unless the user accepts external processing by Zhipu. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jaredforreal/glmv-prompt-gen) <br>
- [Project homepage from skill metadata](https://github.com/zai-org/GLM-V/tree/main/skills/glmv-prompt-gen) <br>
- [Zhipu API keys](https://bigmodel.cn/usercenter/proj-mgmt/apikeys) <br>
- [Zhipu chat completions API documentation](https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E5%AF%B9%E8%AF%9D%E8%A1%A5%E5%85%A8) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style prompt text, with optional saved text file output and JSON-formatted error responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZHIPU_API_KEY; supports image, video, and auto output modes; image and video inputs are mutually exclusive.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
