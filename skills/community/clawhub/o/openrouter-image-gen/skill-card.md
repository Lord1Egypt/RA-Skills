## Description: <br>
Generate images using Google Gemini via the OpenRouter API, with support for text prompts and optional reference-image guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangwenyu2](https://clawhub.ai/user/yangwenyu2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate image files from natural-language prompts, or to guide generation with a reference image. It is useful for illustrations, covers, avatars, and other visual assets when an OpenRouter API key is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and optional reference images are sent to OpenRouter for image generation, which can expose sensitive text, private images, secrets, or proprietary designs. <br>
Mitigation: Use the skill only with content suitable for OpenRouter processing, avoid confidential inputs, and use an API key with spending limits where possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yangwenyu2/openrouter-image-gen) <br>
- [OpenRouter API endpoint](https://openrouter.ai/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Image file output with console status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an OpenRouter API key; saves generated images to the requested local path and may write a debug JSON file when no image is returned.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
