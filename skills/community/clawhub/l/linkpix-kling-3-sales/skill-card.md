## Description:

Helps ecommerce and content teams create product-promotion videos from product images and selling points using Kling 3.0 through qhkit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Ecommerce operators, short-video teams, and brand content teams use this skill to plan and generate product showcase and advertising videos from product images and selling points.

### Deployment Geography for Use:

Global; the skill connects to the iqinghu.com China service.

## Known Risks and Mitigations:

Risk: Installing qhkit may change the user's Node or qhkit environment.

Mitigation: Review npm installation and any user-level environment changes before proceeding.

Risk: An API token is needed to access the video service.

Mitigation: Use a trusted credential setup path and avoid exposing the token in shared output.

Risk: Submitting a video-generation task consumes account credits.

Mitigation: Check the credit estimate and confirm the parameters and cost with the user before submission.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/linkpix-kling-3-sales)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [iqinghu.com API key setup guide](https://xcnzsfe4uxrw.feishu.cn/wiki/KJ0Ywsyw8iAXmRkz5l4cddDbn6g)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with video prompts, generation commands, and resulting video links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video generation requires reference images, an API token, and user confirmation before spending credits.]

## Skill Version(s):

0.1.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
