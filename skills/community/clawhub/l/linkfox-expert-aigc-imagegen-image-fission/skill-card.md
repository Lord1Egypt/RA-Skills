## Description:

电商图片裂变。将已有商品图裂变为视觉不同但商品不变的新图片（相似度可控），用于多平台多店铺铺货防关联。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce operators and listing agents use this skill to create visually differentiated versions of existing product listing images while keeping the product unchanged. It supports single-image and batch workflows for multi-store and multi-platform publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product images, prompts, and account credentials are sent to LinkFox services during image generation, upload, authentication, and billing flows.

Mitigation: Use non-sensitive test assets first, confirm the LinkFox service relationship is acceptable for the deployment, and keep API keys out of logs, chat transcripts, shell history, and startup files.

Risk: Local image files may become publicly accessible after upload.

Mitigation: Upload only files that are approved for public sharing and review generated public URLs before using them in downstream workflows.

Risk: Endpoint override environment variables can redirect requests away from the expected LinkFox gateway.

Mitigation: Set endpoint override variables only in controlled environments and review them before running the skill.

Risk: Similarity reduction is a prompt constraint rather than a measured guarantee.

Mitigation: Manually review output similarity and target-platform compliance before publishing generated listing images.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-expert-aigc-imagegen-image-fission)
- [Image Fission Workflow](references/workflow.md)
- [Image Fission Data Fields](references/data-fields.md)
- [AI Image Generation API Reference](skills/linkfox-aigc-imagegen/references/api.md)
- [Authentication and Billing Onboarding](skills/linkfox-aigc-imagegen/references/onboarding.md)
- [File Upload API Reference](skills/linkfox-file-upload/references/api.md)

## Skill Output:

**Output Type(s):** [Files, Markdown, Shell commands, Guidance]

**Output Format:** [Generated image files with a Markdown original-to-result mapping table and error notes when generation fails]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include public HTTPS image URLs, local media file paths, and status/error details from LinkFox image generation and upload flows.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
