## Description: <br>
Text-to-image and image-to-image generation using MiniMax API that generates images from text prompts (t2i) or transforms reference images (i2i) using MiniMax's image-01 or image-01-live models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanhaixuan](https://clawhub.ai/user/lanhaixuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate images from text prompts or transform reference images with MiniMax image models. It supports terminal and Python use, including model, aspect ratio, style, response format, seed, and save options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and reference images are sent to MiniMax for generation. <br>
Mitigation: Avoid confidential text or images and use only data approved for transfer to MiniMax. <br>
Risk: Using the MiniMax API key may consume paid credits. <br>
Mitigation: Use an account-controlled API key and monitor usage and balance before running large generations. <br>
Risk: The optional save path can write generated image files locally. <br>
Mitigation: Use the default save directory or a deliberate output path to avoid overwriting local files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lanhaixuan/minimax-image-generator) <br>
- [MiniMax platform](https://platform.minimaxi.com) <br>
- [MiniMax Coding Plan subscription](https://platform.minimaxi.com/subscribe/coding-plan) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Shell commands, Code] <br>
**Output Format:** [JSON with image URL or base64 fields, plus an optional saved image file path when saving is requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, requests, and MINIMAX_API_KEY. Prompts are limited to 1500 characters, generation count is 1-9 images, and optional image-to-image inputs may be URLs or base64 data URLs.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
