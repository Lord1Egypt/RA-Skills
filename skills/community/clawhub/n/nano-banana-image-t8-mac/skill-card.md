## Description: <br>
Helps an agent run Nano Banana/T8Star text-to-image and image-to-image generation using a user-provided prompt, optional input images, and an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flywhale-666](https://clawhub.ai/user/flywhale-666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative users use this skill to generate or edit images through the Nano Banana/T8Star service from an agent chat, while reusing saved model and API-key settings when available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected images can be sent to the external service at https://ai.t8star.cn. <br>
Mitigation: Use the skill only with content approved for that service and confirm the intended image inputs before execution. <br>
Risk: The Nano Banana API key can be saved locally for reuse. <br>
Mitigation: Use a dedicated key when possible and delete ~/.whaleclaw/credentials/nano_banana_api_key.txt when saved-key reuse is no longer desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/flywhale-666/nano-banana-image-t8-mac) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Markdown with concise status text, shell command examples, and local image file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated images are saved under the configured local output directory, defaulting to ~/.whaleclaw/workspace/nano_banana_test.] <br>

## Skill Version(s): <br>
0.1.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
