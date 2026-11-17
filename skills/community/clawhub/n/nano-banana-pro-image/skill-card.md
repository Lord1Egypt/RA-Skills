## Description:

Nano Banana Pro Image Generation & Editing helps agents generate and edit professional images through the Atlas Cloud API using Google's Nano Banana Pro models, with support for text-to-image, image editing, reference images, high-resolution outputs, and text-heavy visual assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xixihhhh](https://clawhub.ai/user/xixihhhh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to generate, edit, and download professional visual assets such as marketing images, infographics, menus, diagrams, product photography, concept art, and AI art through Atlas Cloud image models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts and image URLs or image data to Atlas Cloud for image generation and editing.

Mitigation: Use it only with prompts and images that are acceptable for third-party transfer, and confirm the required ATLASCLOUD_API_KEY is managed through environment variables.

Risk: The skill downloads server-provided output URLs without validating that they point to documented Atlas-controlled HTTPS asset domains.

Mitigation: Review before installation and prefer a version that restricts download URL scheme and host before saving generated outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xixihhhh/skills/nano-banana-pro-image)
- [Atlas Cloud](https://www.atlascloud.ai)
- [Atlas Cloud image generation endpoint](https://api.atlascloud.ai/api/v1/model/generateImage)
- [Atlas Cloud prediction endpoint](https://api.atlascloud.ai/api/v1/model/prediction/{prediction-id})

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Files]

**Output Format:** [Markdown guidance with shell commands and downloaded image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ATLASCLOUD_API_KEY and network access to Atlas Cloud API endpoints.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
