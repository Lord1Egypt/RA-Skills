## Description:

Generates Shopee-ready product image sets, detail images, and promotional creatives from product photos through LinkPix.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Shopee sellers and Southeast Asian ecommerce operators use this skill to create localized product listing images, detail graphics, and campaign visuals from product photos.

### Deployment Geography for Use:

Southeast Asia

## Known Risks and Mitigations:

Risk: Setup asks users to share an API key in conversation.

Mitigation: Do not send API keys in chat; enter them through a trusted local secret method.

Risk: The skill can install unpinned packages that may change and run with local permissions.

Mitigation: Review and pin package versions before installation, and limit their local access.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-shopee-image)
- [qhkit package on npm](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Image assets, Guidance]

**Output Format:** [Generated product images returned as image URLs, with concise usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image count, platform, model, and visual options vary by request.]

## Skill Version(s):

0.1.5 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
