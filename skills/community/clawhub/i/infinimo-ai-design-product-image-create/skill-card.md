## Description:

Generate e-commerce product images for hero, secondary, and A+ detail use cases via Infinimo AI Design with marketplace selection, model, aspect, resolution, reference upload, job submission, and result polling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and e-commerce operators use this skill to generate marketplace-ready product images for Amazon, Shopify, and similar listing workflows. It supports choosing platform and market settings, uploading reference images, submitting generation jobs, and polling for output URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reference uploads can send a selected local file to the external Infinimo service without independently verifying that the file is an image.

Mitigation: Only pass intended, non-sensitive image files to upload.sh, and do not allow untrusted instructions to choose local file paths.

Risk: Product images, prompts, and job metadata are sent to Infinimo/clawec.com.

Mitigation: Use this skill only when the release operator trusts that external service with the submitted assets and generation details.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/anyunzhong/skills/infinimo-ai-design-product-image-create)
- [Infinimo AI Design](https://design.infinimo.ai/?source=q-i-d-clawhub)
- [Product Image Design Response Schema](references/response-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return generated image URLs after polling the Infinimo API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
