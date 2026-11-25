## Description:

帮助品牌团队和电商创作者通过青虎 AI 使用 Seedance 2.5 生成商品宣传与带货短视频。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External brand teams, ecommerce designers, and performance marketers use the skill to turn product images and selling points into Seedance 2.5 promotional videos, then track generation and retrieve the finished video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup guidance asks users to share an API key in chat, which could expose account access.

Mitigation: Keep the key out of chat and store it in an environment variable or secure local configuration.

Risk: Unpinned packages may run with the agent's permissions.

Mitigation: Review and pin package versions, and run with only the permissions needed for the task.

Risk: The security scan was partial and missed four referenced paths, so its coverage is incomplete.

Mitigation: Review the referenced files that were not included in the scan before installation.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/autoagc/skills/linkpix-seedance-25-sales)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Video, Shell commands, Configuration guidance]

**Output Format:** [Generated video files with task status and supporting CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Videos are generated from product images and prompts; task details support status tracking and retrieval.]

## Skill Version(s):

0.1.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
