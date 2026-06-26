## Description: <br>
Generate or edit AI images via Pixmind API (text-to-image and image-to-image). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuyunzhishang](https://clawhub.ai/user/fuyunzhishang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate, edit, vary, or upscale images through Pixmind models from natural-language prompts and optional reference image URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, generation settings, and reference image URLs are sent to Pixmind's external API. <br>
Mitigation: Avoid confidential prompts and private or internal image URLs; use the skill only when sending this content to Pixmind is acceptable. <br>
Risk: The skill requires a sensitive Pixmind API key and can consume API credits. <br>
Mitigation: Use a dedicated, revocable API key stored in PIXMIND_API_KEY and monitor API credit usage. <br>
Risk: Generated images are returned as URLs from Pixmind's CDN. <br>
Mitigation: Review generated images and URLs before sharing them or using them in downstream workflows. <br>


## Reference(s): <br>
- [Pixmind](https://www.pixmind.io) <br>
- [Pixmind API Keys](https://www.pixmind.io/api-keys) <br>
- [Pixmind Image Generation Endpoint](https://aihub-admin.aimix.pro/open-api/v1/image/generate) <br>
- [Pixmind Task Status Endpoint](https://aihub-admin.aimix.pro/open-api/v1/task/<TASK_ID>) <br>
- [Pixmind Image on ClawHub](https://clawhub.ai/fuyunzhishang/pixmind-image) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON API responses, task IDs, and generated image URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PIXMIND_API_KEY. Prompts, generation settings, and optional reference image URLs are sent to Pixmind; completed generations return image URLs from Pixmind's CDN.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
