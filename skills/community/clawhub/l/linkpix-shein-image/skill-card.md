## Description:

Creates SHEIN-ready apparel imagery, including model looks, flat lays, detail shots, product carousels, detail pages, and promotional graphics, through Qinghu AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External apparel sellers use this skill to create SHEIN-oriented product imagery, including model photos, flat lays, detail views, carousels, product detail images, and campaign graphics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sharing an API key in chat could expose account access.

Mitigation: Store the key locally through a protected environment or secret mechanism, and rotate any key already shared.

Risk: The external qhkit CLI is installed separately, can change over time, and was not bundled or audited in this review.

Mitigation: Review dependency versions and control upgrades before use.

Risk: Reference images are uploaded to Qinghu, and approved generation consumes credits.

Mitigation: Upload only images you are authorized to share, and review the generation request before approval.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-shein-image)
- [Publisher profile (autoagc)](https://clawhub.ai/user/autoagc)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Images, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance and qhkit shell commands; generated images are returned as URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image generation requires a configured qhkit account and reference images or custom copy where applicable.]

## Skill Version(s):

0.1.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
