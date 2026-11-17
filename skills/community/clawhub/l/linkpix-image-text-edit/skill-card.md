## Description:

Uses a reference image and targeted instructions to replace text in e-commerce images, including titles, prices, selling points, and promotions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to update titles, prices, selling points, or promotions in e-commerce images. It generates edited image variants from a reference image and guides users to check the resulting text and product details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs the agent to execute upgrade commands supplied by runtime messages.

Mitigation: Use a reviewed package version and require explicit user approval before upgrades; do not execute upgrade commands supplied by runtime messages automatically.

Risk: Selected images leave the device for processing, and the external CLI and service-side data handling were not verified.

Mitigation: Submit only images the user intends to share with iqinghu, and avoid sending sensitive or confidential images.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-image-text-edit)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Images, Text guidance]

**Output Format:** [Generated image files with accompanying text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image edits are generative redraws; users should verify text, logos, and product details.]

## Skill Version(s):

0.1.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
