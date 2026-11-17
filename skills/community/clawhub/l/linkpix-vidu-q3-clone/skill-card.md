## Description:

Helps sellers adapt the camera work and pacing of a reference short video into a product-specific script and generate a Vidu Q3 video through Qinghu AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Sellers and content creators use this skill to analyze a reference short video, rewrite its shot structure for their own products, and generate a promotional video after approving the script and expected credit charge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic installation or upgrades may run unpinned packages and change local tool configuration or PATH.

Mitigation: Review installation steps and prefer a preinstalled, pinned qhkit version in an isolated environment.

Risk: The workflow sends an API key and uploaded media to Qinghu services.

Mitigation: Use an appropriately scoped key and share only media approved for upload.

Risk: Video generation spends account credits and submitted tasks cannot be canceled.

Mitigation: Confirm the model, inputs, duration, and estimated credits with the user before submission.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-vidu-q3-clone)
- [Qinghu qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API key guide](https://xcnzsfe4uxrw.feishu.cn/wiki/KJ0Ywsyw8iAXmRkz5l4cddDbn6g)

## Skill Output:

**Output Type(s):** [Text, Video links]

**Output Format:** [Markdown with original and adapted scripts, followed by a generated video URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the task ID and credits charged; generation requires user confirmation.]

## Skill Version(s):

0.1.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
