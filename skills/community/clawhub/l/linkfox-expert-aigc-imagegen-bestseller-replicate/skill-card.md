## Description:

Generates batches of ecommerce product images by applying the layout and visual style of Amazon listing images or user-supplied bestseller references to the user's product image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce sellers and operators use this skill to create a reference-to-replica image set for product listings. It supports either an Amazon ASIN/listing workflow or a user-uploaded reference-image workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product and reference images may be uploaded to public OSS URLs or sent to LinkFox services.

Mitigation: Use only non-sensitive images and confirm that files are acceptable for public URL access before running upload-dependent paths.

Risk: Amazon ASIN lookup and image generation can consume paid service credits.

Mitigation: Confirm paid lookups and generation scope before running, especially when including A+ images or many references.

Risk: Credential and endpoint variables can affect external service calls.

Mitigation: Run in a trusted environment, keep LINKFOX credentials scoped, and avoid allowing untrusted projects or wrappers to set LINKFOX_* endpoint variables.

Risk: Generated product-listing images may be inaccurate, misleading, or unsuitable for marketplace policy requirements.

Mitigation: Review outputs before publication and verify that claims, visuals, and platform compliance requirements are satisfied.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/linkfox-ai/skills/linkfox-expert-aigc-imagegen-bestseller-replicate)
- [Bestseller replicate workflow](artifact/references/workflow.md)
- [Bestseller replicate data fields](artifact/references/data-fields.md)
- [Image generation API reference](artifact/skills/linkfox-aigc-imagegen/references/api.md)
- [Amazon product detail API reference](artifact/skills/linkfox-amazon-product-detail/references/api.md)
- [File upload API reference](artifact/skills/linkfox-file-upload/references/api.md)

## Skill Output:

**Output Type(s):** [files, markdown, text, guidance]

**Output Format:** [Generated image files with a Markdown reference-to-replica comparison table and failure notes when applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One generated image per reference image; Amazon listing mode may include main images and A+ images by default.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
