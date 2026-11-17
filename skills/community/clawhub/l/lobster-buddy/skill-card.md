## Description:

麻薯的电子宠物系统。基于用户ID确定性生成的RPG风格宠物，有物种、稀有度、属性和闪光机制。当用户问"我的宠物"、"看看我的buddy"、"抽宠物"时触发。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiaofei860208-source](https://clawhub.ai/user/wangxiaofei860208-source)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to add a persistent RPG-style electronic pet to agent conversations, including pet display, custom naming, and occasional pet comments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill keeps a small persistent pet profile tied to the user ID.

Mitigation: Disclose the local memory behavior before deployment and allow users or operators to review or remove the stored pet profile.

Risk: The pet may occasionally add comments to replies.

Mitigation: Keep trigger and participation behavior clear so users understand when the pet persona may appear.

## Reference(s):

- [Lobster Buddy ClawHub release](https://clawhub.ai/wangxiaofei860208-source/skills/lobster-buddy)
- [Publisher profile](https://clawhub.ai/user/wangxiaofei860208-source)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown text with pet status panels and conversational comments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May keep a small local pet profile tied to the user ID.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
