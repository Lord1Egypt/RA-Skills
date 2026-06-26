## Description: <br>
Generate images using MiniMax API (image-01 model) with automatic prompt optimization for better results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lilmrmeeseeks](https://clawhub.ai/user/lilmrmeeseeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate images from Chinese or English prompts through the MiniMax image-01 model. The skill rewrites prompts with style, lighting, and quality terms before requesting one 16:9 image. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts may contain private or confidential text that is rewritten, logged locally, and sent to MiniMax. <br>
Mitigation: Do not include secrets or confidential details in prompts; use a scoped API key if available. <br>
Risk: The skill depends on a MiniMax or AIMLAPI API key to call an external image-generation service. <br>
Mitigation: Install only when MiniMax image generation is intended and manage API keys through environment variables. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lilmrmeeseeks/openclaw-minimax-img) <br>
- [MiniMax image generation API endpoint](https://api.minimaxi.com/v1/image_generation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown] <br>
**Output Format:** [Markdown text with an optimized prompt and generated image link; may also include an image attachment.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns one 16:9 image request by default and requires MINIMAX_API_KEY or AIMLAPI_API_KEY.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
