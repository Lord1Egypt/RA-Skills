## Description:

Guides agents through creating Vidu Q2 product videos from product images and selling points using Qinghu's video tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce merchants, designers, and store operators use this skill to plan and generate short product showcase and advertising videos from product images and selling points.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the required npm tool and configuring a local API token exposes the environment to third-party tooling and credential handling.

Mitigation: Review the package before installation and keep the API token private in local configuration.

Risk: Selected product images or videos are uploaded to Qinghu for generation.

Mitigation: Upload only media authorized for sharing with Qinghu.

Risk: Video generation consumes credits and cannot be cancelled after submission.

Mitigation: Check the estimate and confirm the model, duration, media, and expected cost before submitting.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-vidu-q2-sales)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API key setup](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown]

**Output Format:** [Markdown with command examples, task status, and video links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a video task ID, estimated or charged credits, and a generated video URL.]

## Skill Version(s):

0.1.4 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
