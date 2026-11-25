## Description:

Creates e-commerce product videos through Qinghu AI, using Vidu Q3 when available to preserve reference-image details and suggesting similar models when it is not.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce sellers, designers, and storefront operators use the skill to turn product images and selling points into short promotional videos, with a focus on preserving product materials, patterns, and packaging details.

### Deployment Geography for Use:

China (the documented Qinghu integration uses its domestic service)

## Known Risks and Mitigations:

Risk: Setup instructions install an unpinned package, which may change without review.

Mitigation: Review the package and pin an approved version before installation.

Risk: The setup instructions ask users to share an API key in chat.

Mitigation: Collect credentials through a secure local prompt or secret manager instead of chat.

## Reference(s):

- [qhkit package on npm](https://www.npmjs.com/package/@iqinghu/qhkit)
- [LinkPix Vidu Q3 skill release](https://clawhub.ai/autoagc/skills/linkpix-vidu-q3-sales)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, Video]

**Output Format:** [Markdown guidance and JSON command parameters; generated video results are returned as task status and video links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video generation requires a configured Qinghu API credential and consumes credits; model and option labels are selected from the live catalog.]

## Skill Version(s):

0.1.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
