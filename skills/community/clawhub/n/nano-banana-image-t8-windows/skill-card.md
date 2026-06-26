## Description: <br>
Helps an agent call the Nano Banana/T8 image API to generate or edit images from prompts and optional input images, saving output files locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flywhale-666](https://clawhub.ai/user/flywhale-666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to test text-to-image and image-to-image generation against the Nano Banana/T8 service using a supplied API key, prompt, optional aspect ratio or size, and optional source images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and uploaded images are sent to an external Nano Banana/T8 image-generation API. <br>
Mitigation: Use the skill only with a trusted provider, avoid private images or sensitive prompts, and confirm the configured endpoint before execution. <br>
Risk: The skill can reuse an API key stored locally for later image-generation calls. <br>
Mitigation: Use a dedicated, revocable API key and delete ~/.whaleclaw/credentials/nano_banana_api_key.txt when persistent reuse is no longer desired. <br>


## Reference(s): <br>
- [ClawHub release: Nano Banana Image T8](https://clawhub.ai/flywhale-666/nano-banana-image-t8-windows) <br>
- [Publisher profile: flywhale-666](https://clawhub.ai/user/flywhale-666) <br>
- [Nano Banana/T8 API endpoint](https://ai.t8star.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown with inline shell commands, local file paths, and structured error details when calls fail] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated image file paths, HTTP status details, request URLs, response bodies, and API key reuse guidance.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
