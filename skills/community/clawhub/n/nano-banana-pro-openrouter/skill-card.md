## Description: <br>
Generate images with Nano Banana Pro via OpenRouter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DuffyCoder](https://clawhub.ai/user/DuffyCoder) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to generate new PNG images from text prompts through OpenRouter's Nano Banana Pro image model. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an OpenRouter API key for billed image-generation requests. <br>
Mitigation: Use a dedicated limited key, keep the .env scoped to OPENROUTER_API_KEY and OPENROUTER_BASE_URL, and confirm the base URL points to the intended provider endpoint. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/DuffyCoder/nano-banana-pro-openrouter) <br>
- [OpenRouter Chat Completions Endpoint](https://openrouter.ai/api/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; generated PNG files and MEDIA_URL file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports 1K, 2K, and 4K generation; saves images under ~/.openclaw/workspace/outputs/nano-banana-pro-openrouter; shell version does not support image editing.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
