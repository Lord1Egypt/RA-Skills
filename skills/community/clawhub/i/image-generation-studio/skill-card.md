## Description: <br>
Generate or edit images with the image-generation-studio CLI through supported Gemini, OpenAI Images, OpenAI Responses, xAI, and custom provider configurations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[limkim0530](https://clawhub.ai/user/limkim0530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and other agent users use this skill to generate, edit, compose, or restyle images through configured image providers while keeping provider, model, endpoint, and credential choices explicit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected input images are sent to the configured image provider. <br>
Mitigation: Use only providers and endpoints trusted for the data being processed, and avoid submitting sensitive image or prompt content unless that provider is approved for it. <br>
Risk: API keys may be supplied through command-line flags, environment variables, or local config. <br>
Mitigation: Prefer provider-specific environment variables over storing keys in config.json, and use the config discovery command that redacts credential values. <br>
Risk: Some providers may return temporary image URLs for download. <br>
Mitigation: Prefer b64_json responses when supported and use trusted HTTPS provider endpoints to reduce exposure to arbitrary provider-returned URLs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/limkim0530/image-generation-studio) <br>
- [Gemini adapter](references/adapter-gemini.md) <br>
- [OpenAI Images-compatible adapter](references/adapter-openai-images.md) <br>
- [OpenAI Responses adapter](references/adapter-openai-responses.md) <br>
- [Configuration assistant](references/configuration.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown with inline bash commands and saved image file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save generated or edited images as PNG, JPEG, or WEBP depending on the requested filename and provider response.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
