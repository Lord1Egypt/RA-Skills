## Description:

Generates Seedream 5.0 e-commerce images from text prompts or reference images for product listings and campaign graphics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce designers, product photographers, brand teams, and marketing operators use this skill to create product images and campaign graphics from text prompts or reference photos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance requests an API key in chat, which could expose the credential.

Mitigation: Configure the key locally with qhkit or an environment variable; do not post it in chat, and rotate it if it has already been shared.

Risk: The workflow installs and upgrades external software, whose package code and publisher provenance were not independently verified.

Mitigation: Use reviewed package versions and controlled updates before installing or upgrading.

Risk: Product images and details may be sent to an external service, including during prompt polishing.

Mitigation: Provide only images and product details that you are authorized to share with that service.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-seedream-5-pro)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [API key setup guide](https://xcnzsfe4uxrw.feishu.cn/wiki/KJ0Ywsyw8iAXmRkz5l4cddDbn6g)

## Skill Output:

**Output Type(s):** [Images, Guidance]

**Output Format:** [Generated image files or image URLs, with text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports text prompts and optional reference images; image count, model, and size depend on the available service options.]

## Skill Version(s):

0.1.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
