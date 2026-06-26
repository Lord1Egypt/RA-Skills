## Description: <br>
Generate/edit images with Nano Banana Pro (Gemini 3 Pro Image) via OpenRouter. Use for image create/modify requests incl. edits. Supports text-to-image + image-to-image; 1K/2K/4K; use --input-image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liberalchang](https://clawhub.ai/user/liberalchang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate new PNG images or edit existing images through OpenRouter, choosing 1K, 2K, or 4K output and optionally supplying an input image for image-to-image edits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected input images are transmitted to OpenRouter and the underlying model provider. <br>
Mitigation: Avoid confidential, regulated, or personal images unless that external transfer is acceptable for the use case. <br>
Risk: The skill requires an OpenRouter API key for generation or editing. <br>
Mitigation: Prefer setting OPENROUTER_KEY in the environment instead of passing API keys in chat or command arguments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liberalchang/nanobanana-openrouter) <br>
- [OpenRouter API endpoint used by the script](https://openrouter.ai/api/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, Files] <br>
**Output Format:** [Markdown guidance with shell command examples; scripts print generated image paths and save PNG files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports prompt text, optional input image path, filename, output directory, API key source, and 1K/2K/4K resolution.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
