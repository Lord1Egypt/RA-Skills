## Description:

Helps commerce teams create product and advertising videos with HappyHorse 1.1 using text prompts and optional image, video, or audio references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Commerce and brand teams use this skill to plan and generate short product demonstrations and promotional videos from prompts and optional media references, then receive the resulting video links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup or upgrades may change the user's local Node/npm environment.

Mitigation: Review the requested installation and prefer manually installing pinned tool versions.

Risk: Configuring qhkit may expose an API key if the user pastes it into chat.

Mitigation: Set the key through a secure local secret mechanism instead of sharing it in chat.

Risk: Video generation consumes credits and submitted tasks cannot be canceled.

Mitigation: Confirm the model, inputs, duration, and estimated credit cost with the user before submitting a task.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/linkpix-happyhorse-sales)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API key guide](https://xcnzsfe4uxrw.feishu.cn/wiki/KJ0Ywsyw8iAXmRkz5l4cddDbn6g)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Video links]

**Output Format:** [Markdown with video URLs and task details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the task ID and credit usage; generated videos are accessed through returned URLs.]

## Skill Version(s):

0.1.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
