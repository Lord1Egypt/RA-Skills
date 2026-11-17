## Description:

Creates Wildberries product image sets, detail graphics, and campaign visuals with Russian-language layouts using Qinghu AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Wildberries sellers and cross-border ecommerce teams use this skill to create product image sets, detail graphics, and campaign visuals for Russian-speaking shoppers.

### Deployment Geography for Use:

Russia and other CIS markets

## Known Risks and Mitigations:

Risk: Setup instructions ask users to send an account API key in chat.

Mitigation: Configure a restricted Qinghu API key locally instead of sharing it in chat, and rotate any key already shared.

Risk: Image generation sends submitted images for external processing.

Mitigation: Use only images approved for external processing.

Risk: The CLI version and automatic upgrade behavior can affect operation.

Mitigation: Review the CLI version and automatic upgrade behavior before use.

Risk: Image generation can incur credit charges.

Mitigation: Confirm the estimated credit charge before generation.

## Reference(s):

- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [LinkPix ClawHub release](https://clawhub.ai/autoagc/skills/linkpix-wildberries-image)

## Skill Output:

**Output Type(s):** [Images, Guidance]

**Output Format:** [Generated image assets with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Product image sets, detail graphics, and campaign visuals; image options and quality depend on the selected generation mode.]

## Skill Version(s):

0.1.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
