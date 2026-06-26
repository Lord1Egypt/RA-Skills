## Description: <br>
Generates and reimagines PNG images through the xAI Grok/Flux image API using prompts, styles, aspect ratios, batch counts, and base64 responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NixeiFoit](https://clawhub.ai/user/NixeiFoit) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to generate new images or create style-transfer and reimagined variants of source images from natural-language prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, selected local images, or supplied image URLs are sent to xAI for image generation or reimagination. <br>
Mitigation: Use only data appropriate for xAI processing; avoid confidential files, private URLs, and non-image sources. <br>
Risk: Image editing is reimagination or style transfer, not pixel-precise inpainting. <br>
Mitigation: Review generated outputs before use and do not rely on the skill for exact localized edits. <br>
Risk: The skill depends on an xAI API key and external API behavior. <br>
Mitigation: Confirm XAI_API_KEY is available in the target environment and handle API moderation, failures, or policy changes before deployment. <br>


## Reference(s): <br>
- [xAI Images API endpoint](https://api.x.ai/v1/images/generations) <br>
- [ClawHub skill listing](https://clawhub.ai/NixeiFoit/grok-imagine-image-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with bash and Python snippets plus generated PNG file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires XAI_API_KEY, curl, and python3; generated images are saved under ~/.openclaw/media/.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
