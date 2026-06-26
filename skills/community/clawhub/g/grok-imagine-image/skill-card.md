## Description: <br>
Generate images with xAI Grok Imagine models, including batch generation, aspect ratios, base64 output, and concurrent requests through the xAI API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maliot100x](https://clawhub.ai/user/maliot100x) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and content teams use this skill to generate AI images from text prompts with xAI Grok Imagine models, including single images, variations, and base64 outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to an xAI API key and sends image prompts to xAI. <br>
Mitigation: Provide the key only in a controlled environment, monitor API usage and costs, and avoid submitting prompts that contain sensitive information. <br>
Risk: Generated image URLs may be temporary. <br>
Mitigation: Download needed outputs promptly or request base64 output when embedding or retaining generated images. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maliot100x/grok-imagine-image) <br>
- [xAI image generation documentation](https://docs.x.ai/developers/model-capabilities/images/generation) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with curl, JSON, and SDK code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses XAI_API_KEY and may return temporary image URLs or base64 image data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
