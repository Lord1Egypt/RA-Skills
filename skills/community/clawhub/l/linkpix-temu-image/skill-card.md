## Description:

Creates Temu-ready product image sets, detail graphics, and promotional posters from product images and copy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers use this skill to create Temu listing and campaign visuals, including main image sets, detail graphics, and promotional posters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow requests API keys in chat and directs automatic installation and upgrading of executable packages.

Mitigation: Set credentials locally through a protected environment or secret store. Review and pin dependency versions, and approve upgrades.

Risk: Selected product images leave the user's machine for processing.

Mitigation: Submit only images approved for external processing.

Risk: Image generation spends credits.

Mitigation: Review the estimate and require confirmation before submitting a generation task.

## Reference(s):

- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [ClawHub skill page](https://clawhub.ai/autoagc/skills/linkpix-temu-image)

## Skill Output:

**Output Type(s):** [Images, Text]

**Output Format:** [Generated image files or URLs with concise task status and credit details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce a main image set, a detail graphic, or a promotional poster; image count and quality follow the selected options.]

## Skill Version(s):

0.1.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
