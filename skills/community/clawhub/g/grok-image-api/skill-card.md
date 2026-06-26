## Description: <br>
Work with OpenAI-compatible image generation and image editing endpoints. Use when the user wants to generate images from prompts, edit images with prompts and optional masks, test an image endpoint, or integrate /v1/images/generations or /v1/images/edits into scripts or projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[XiaoLozee](https://clawhub.ai/user/XiaoLozee) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to call OpenAI-compatible image generation or image editing endpoints, test endpoint reachability, and save returned images locally for reuse or delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts and optional source images to the configured image API provider. <br>
Mitigation: Use a provider you trust, verify IMAGE_API_BASE_URL before calls, and avoid submitting private images unless the provider's handling is acceptable. <br>
Risk: The helper requires an API key and attaches it to outbound requests. <br>
Mitigation: Use a dedicated or scoped API key where possible, provide it through environment variables, and avoid echoing secrets in chat or committed files. <br>
Risk: Generated or edited images are saved locally and may overwrite files if an existing output path is reused. <br>
Mitigation: Choose output paths deliberately and review local files before sharing or reusing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/XiaoLozee/grok-image-api) <br>
- [Publisher profile](https://clawhub.ai/user/XiaoLozee) <br>
- [API notes](artifact/references/api-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, API request details, and local image file paths or returned image URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper script can generate, edit, probe, and save images under output/grok-images/ by default; remote image URLs can be preserved when requested.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
