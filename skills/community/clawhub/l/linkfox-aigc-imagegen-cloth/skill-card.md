## Description:

Generates ecommerce clothing images, including ghost-mannequin white-background images, model images, lifestyle images, selling-point images, A+ images, and size-chart images from uploaded clothing or model references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and ecommerce operators use this skill to generate clothing marketing images and coordinated image sets for apparel listings. It supports single-image generation and multi-image planning for common clothing commerce formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles login, API-key, and payment flows.

Mitigation: Install only if LinkFox is trusted, prefer self-service API-key setup, and keep API keys out of logs and shell history.

Risk: Endpoint and script-path flexibility can increase execution risk.

Mitigation: Do not override LINKFOX_* API URLs, and avoid job or state files from untrusted sources until script-path validation is fixed.

Risk: Phone or SMS login can expose account access if initiated unexpectedly.

Mitigation: Do not enter a phone number or SMS code unless you initiated the login flow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-aigc-imagegen-cloth)
- [Runtime index](artifact/references/runtime/00-index.md)
- [Image delivery protocol](artifact/references/runtime/03-deliver.md)
- [White-background clothing image reference](artifact/references/types/white-bg.md)
- [Model clothing image reference](artifact/references/types/model-image.md)
- [Lifestyle clothing image reference](artifact/references/types/scene.md)
- [Selling-point clothing image reference](artifact/references/types/selling-point.md)
- [A+ clothing image reference](artifact/references/types/aplus.md)
- [Size-chart clothing image reference](artifact/references/types/size.md)
- [Authentication and billing onboarding](artifact/references/onboarding.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON, image files]

**Output Format:** [Markdown responses with inline image links, JSON state files, shell commands, and generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce one image or a coordinated image set; image generation depends on LinkFox credentials, model selection, and user-supplied clothing or model image URLs.]

## Skill Version(s):

1.2.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
