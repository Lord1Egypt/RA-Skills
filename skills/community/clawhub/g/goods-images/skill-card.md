## Description:

Generates e-commerce product carousel and detail images from product photos or descriptions for marketplaces such as Taobao, Tmall, and JD.

This skill is ready for commercial/non-commercial use.

## Publisher:

[briefness](https://clawhub.ai/user/briefness)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, marketers, and e-commerce operators use this skill to create product marketing image sets from uploaded product photos or product descriptions. The workflow plans and generates carousel images, detail-page images, promotional overlays, and a final image list for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may install an unpinned package during execution.

Mitigation: Review the package installation step before use and run the skill only where automatic package installation is acceptable.

Risk: Product images are stored in a shared temporary folder.

Mitigation: Avoid confidential product images in shared, sensitive, or production environments and clear temporary files after use.

Risk: Generated product depictions may be inaccurate or alter product presentation.

Mitigation: Manually review generated images for product fidelity and marketing accuracy before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/briefness/skills/goods-images)

## Skill Output:

**Output Type(s):** [Files, Images, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Generated image files with a Markdown image list and optional Python/PIL commands for text and logo overlays.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normally produces up to 14 images: five 800x800 carousel images and nine product detail images around 790x1100.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
