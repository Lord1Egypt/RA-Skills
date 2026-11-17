## Description:

Helps e-commerce teams adapt the structure of popular short videos into product-focused scripts and generate videos through Qinghu AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce video teams use this skill to analyze a reference clip, adapt its pacing and selling points to their product, and request a short video suited to Taobao channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation may run unpinned external npm or npx packages.

Mitigation: Review the package before installation and prefer a preinstalled, pinned qhkit version.

Risk: Configuring qhkit requires an API token.

Mitigation: Use a scoped or revocable key and avoid sharing a long-lived secret in chat.

Risk: Video generation spends credits and submitted tasks cannot be cancelled.

Mitigation: Estimate credits and confirm the script and generation settings with the user before submission.

Risk: Recreating a reference video may copy protected footage or dialogue.

Mitigation: Adapt only the structure and creative approach; do not reuse original footage or dialogue without permission.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-wanx-3-clone)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu AI API key guide](https://xcnzsfe4uxrw.feishu.cn/wiki/KJ0Ywsyw8iAXmRkz5l4cddDbn6g)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with commands, script comparison, task status, and video links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video generation requires user confirmation; completed tasks return a video link and charged credits.]

## Skill Version(s):

0.1.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
