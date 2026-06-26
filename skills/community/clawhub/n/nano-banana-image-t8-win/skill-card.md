## Description: <br>
Uses a provided Nano Banana API key to generate or edit images from text prompts and uploaded images through the T8 image API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flywhale-666](https://clawhub.ai/user/flywhale-666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent users and developers use this skill to run Nano Banana text-to-image and image-to-image generation from conversation parameters, including prompts, optional uploaded images, size or ratio choices, and a user-provided API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a Nano Banana API key locally for reuse. <br>
Mitigation: Use a dedicated API key and delete or rotate ~/.whaleclaw/credentials/nano_banana_api_key.txt when access should end. <br>
Risk: Prompts and uploaded images are sent to the external Nano Banana/T8 API provider. <br>
Mitigation: Submit only prompts and images that are appropriate to share with that provider. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/flywhale-666/nano-banana-image-t8-win) <br>
- [T8 image API service](https://ai.t8star.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Concise Markdown with shell command examples, API status details, and generated image file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a prompt and API key; image editing also requires at least one input image. Generated images are saved under ~/.whaleclaw/workspace/nano_banana_test/ by default.] <br>

## Skill Version(s): <br>
0.1.8 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
