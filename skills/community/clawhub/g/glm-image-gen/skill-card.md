## Description: <br>
Generates images from text prompts using the Zhipu GLM-Image API, with support for multiple aspect ratios, HD quality, watermark control, and optional local saving. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaredforreal](https://clawhub.ai/user/jaredforreal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn text prompts into generated images for illustrations, portraits, social graphics, posters, and concept art through Zhipu's hosted API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, optional user IDs, and API usage are sent to Zhipu's hosted image generation service. <br>
Mitigation: Use only when the user trusts Zhipu with the request, and avoid secrets or sensitive personal data in prompts or --user-id. <br>
Risk: The skill requires ZHIPU_API_KEY, a sensitive credential. <br>
Mitigation: Store the key in the intended environment configuration, protect it like a password, and avoid pasting it into prompts or shared output. <br>
Risk: Generated image URLs are temporary, and --save writes an image to a local path. <br>
Mitigation: Save needed images promptly and use --save only with an intended output path. <br>


## Reference(s): <br>
- [Skill homepage](https://github.com/zai-org/GLM-Image/tree/main/skills/glm-image-gen) <br>
- [Zhipu Image Generation API documentation](https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E5%9B%BE%E5%83%8F%E7%94%9F%E6%88%90) <br>
- [GLM-Image model documentation](https://docs.bigmodel.cn/cn/guide/models/image-generation/glm-image) <br>
- [Zhipu API key management](https://bigmodel.cn/usercenter/proj-mgmt/apikeys) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON CLI results containing generated image URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZHIPU_API_KEY; can optionally save generated images to a local file; returned image URLs are temporary.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
