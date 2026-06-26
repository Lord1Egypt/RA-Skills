## Description: <br>
Generates images locally with Ollama's x/z-image-turbo model on macOS and can send the result through WhatsApp. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Eric51](https://clawhub.ai/user/Eric51) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and end users on macOS use this skill to generate local images from prompts with Ollama, tune size, steps, seed, and negative prompt parameters, and optionally share generated images through WhatsApp. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated images may be sent through WhatsApp without a clear confirmation step. <br>
Mitigation: Require the agent to ask for the WhatsApp recipient and confirm the generated image and caption before every send. <br>
Risk: Verbose execution can log the constructed command, including prompt text. <br>
Mitigation: Avoid sensitive prompts and disable or review verbose logging when handling private content. <br>
Risk: The skill depends on a local macOS Ollama instance and the x/z-image-turbo model. <br>
Mitigation: Verify the host prerequisites and installed model before use, and fail closed if local generation is unavailable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Eric51/ollama-x-z-image-turbo) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with bash commands and generated PNG file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local macOS Ollama setup with the x/z-image-turbo model; WhatsApp sharing should require explicit recipient and send confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
