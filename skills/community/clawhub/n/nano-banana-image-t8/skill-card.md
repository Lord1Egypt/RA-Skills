## Description: <br>
Helps agents call the ai.t8star.cn Nano Banana image API for text-to-image generation and image editing, using a user-provided API key and saving generated images locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flywhale-666](https://clawhub.ai/user/flywhale-666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and image-generation users use this skill to run Nano Banana text-to-image and image-edit tests from conversation parameters, including prompts, optional image inputs, aspect ratios, and model selection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a user-provided Nano Banana API key and may persist it locally. <br>
Mitigation: Use a dedicated limited-use API key, treat it as a secret, and delete or rotate the saved key when it is no longer needed. <br>
Risk: Image-editing mode uploads user-selected image files to the configured Nano Banana API endpoint. <br>
Mitigation: Provide only image paths that are appropriate to upload to the ai.t8star.cn service. <br>


## Reference(s): <br>
- [ClawHub listing: Nano Banana Image T8](https://clawhub.ai/flywhale-666/nano-banana-image-t8) <br>
- [Publisher profile: flywhale-666](https://clawhub.ai/user/flywhale-666) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Guidance] <br>
**Output Format:** [Concise chat responses with shell command execution and local PNG image output paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist the API key and default model under the user's ~/.whaleclaw credentials directory and writes generated images to ~/.whaleclaw/workspace/nano_banana_test by default.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
