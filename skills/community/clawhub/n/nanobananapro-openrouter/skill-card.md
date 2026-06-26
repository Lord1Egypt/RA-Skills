## Description: <br>
Generate/edit images with Nano Banana Pro (Gemini 3 Pro Image) via OpenRouter. Use for image create/modify requests incl. edits. Supports text-to-image + image-to-image; 1K/2K/4K; use --input-image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liberalchang](https://clawhub.ai/user/liberalchang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate new images or edit existing images through OpenRouter using prompt text, optional input images, and selectable 1K, 2K, or 4K output resolution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and supplied input images are sent to OpenRouter and its model providers. <br>
Mitigation: Use only approved content for this workflow and avoid confidential, regulated, or personal images unless that use is explicitly authorized. <br>
Risk: The skill requires an OpenRouter API key. <br>
Mitigation: Prefer the OPENROUTER_KEY environment variable instead of passing keys in chat or command-line arguments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liberalchang/nanobananapro-openrouter) <br>
- [OpenRouter Chat Completions API](https://openrouter.ai/api/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [Image files, Shell commands, Guidance] <br>
**Output Format:** [PNG files saved to disk with console status text and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports text-to-image and image-to-image flows, optional custom output directory, and 1K, 2K, or 4K resolution.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
