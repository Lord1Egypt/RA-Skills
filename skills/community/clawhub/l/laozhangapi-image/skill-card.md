## Description: <br>
Generates and edits images through the laozhang.ai API, including text-to-image, image editing, multi-image fusion, model selection, and aspect-ratio options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[enihsago](https://clawhub.ai/user/enihsago) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agents use this skill to generate new images, edit existing image URLs, apply preset styles, combine multiple images, and save or return generated image assets through Python CLI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, source image URLs, and generated content are sent to laozhang.ai. <br>
Mitigation: Use the skill only when the user accepts sharing those inputs with laozhang.ai and avoid sending sensitive images or prompts. <br>
Risk: API tokens can be exposed if passed directly on the command line. <br>
Mitigation: Prefer storing the token in ~/.laozhang_api_token and avoid placing tokens in prompts, shell history, shared logs, or screenshots. <br>
Risk: Generation and editing calls may create billable API usage, especially with broad trigger phrases. <br>
Mitigation: Confirm intent, model choice, and expected cost before running image generation or editing commands. <br>
Risk: Scripts save image files locally by default unless --no-save is used. <br>
Mitigation: Use --no-save for URL-only workflows or specify an explicit output path when local file placement matters. <br>


## Reference(s): <br>
- [ClawHub Laozhangapi Image listing](https://clawhub.ai/enihsago/laozhangapi-image) <br>
- [Usage Examples](examples/usage.md) <br>
- [Model Details](references/models.md) <br>
- [Laozhang API Documentation](https://docs.laozhang.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with Python CLI commands; scripts can output image URLs, base64 summaries, optional JSON responses, and saved PNG files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The scripts call a third-party API, can read an API token from ~/.laozhang_api_token or --token, and can save generated or edited images under ~/Pictures/laozhang unless --no-save is used.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
