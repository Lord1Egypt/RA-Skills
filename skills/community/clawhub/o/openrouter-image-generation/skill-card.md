## Description: <br>
Generate or edit images through OpenRouter's multimodal image generation endpoint (`/api/v1/chat/completions`) using OpenRouter-compatible image models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Bawerlacher](https://clawhub.ai/user/Bawerlacher) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to generate new images or edit existing images through OpenRouter-compatible image models, with configurable model, aspect ratio, image size, and provider-specific image options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected input images are sent to OpenRouter for generation or editing. <br>
Mitigation: Use a scoped OpenRouter API key and do not provide sensitive prompts or local images unless they are intended to be shared with the provider. <br>
Risk: Generated files may be written outside the expected handoff directory if a different filename path is provided. <br>
Mitigation: Use the recommended outbound media directory or another intentional safe output path. <br>
Risk: Model or provider-specific image configuration may be rejected by OpenRouter. <br>
Mitigation: Remove unsupported image configuration options or switch to a model that supports the requested aspect ratio, image size, and modality. <br>


## Reference(s): <br>
- [OpenRouter image generation documentation](https://openrouter.ai/docs/guides/overview/multimodal/image-generation) <br>
- [OpenRouter chat completions endpoint](https://openrouter.ai/api/v1/chat/completions) <br>
- [ClawHub skill page](https://clawhub.ai/Bawerlacher/openrouter-image-generation) <br>
- [Publisher profile](https://clawhub.ai/user/Bawerlacher) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Files, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; generated PNG image files saved to the requested output path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper prints the saved file path and supports base64 data URL image responses from OpenRouter.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
