## Description:

Creates TikTok Shop product images, carousel sets, detail pages, and campaign graphics from product photos through Qinghu AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

TikTok Shop sellers and social commerce teams use the skill to create product image sets, detail page visuals, and campaign graphics from product photos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance asks users to share a reusable API key in chat.

Mitigation: Configure the key locally through protected secret storage, never paste it into chat, and rotate it if it has already been shared.

Risk: Product images are uploaded to the image service, and generation consumes credits.

Mitigation: Upload only images intended to be shared with the provider and confirm the estimated cost before submitting generation.

Risk: External package behavior and credential storage have not been verified.

Mitigation: Use reviewed dependency versions and control package updates.

## Reference(s):

- [qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [LinkPix skill release on ClawHub](https://clawhub.ai/autoagc/skills/linkpix-tiktok-shop-image)

## Skill Output:

**Output Type(s):** [Images, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Generated image assets delivered as URLs, with Markdown usage guidance and inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image count, model, size, quality, and visual content depend on the selected options and user-provided product images or copy.]

## Skill Version(s):

0.1.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
