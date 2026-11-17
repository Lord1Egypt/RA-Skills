## Description:

使用 Nano Banana 2 把同一授权主体迁移到不同渠道背景，并用背景版本表控制平台、场景、光线、安全区与禁止暗示；通过 AI Hive 编辑指定图片。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, ecommerce operators, and agent users use this skill to move an authorized subject or product image into channel-specific backgrounds while preserving identity, product facts, camera angle, lighting constraints, and composition safety areas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected reference images and prompts are sent to AI Hive for generation.

Mitigation: Use only images you are authorized to edit, avoid sensitive files, and review prompts before submitting them.

Risk: The workflow stores or reads an AI Hive API key locally.

Mitigation: Prefer environment-based secrets where practical and keep local key files restricted to the current user.

Risk: Generated files are downloaded from result URLs into a local output directory.

Mitigation: Use a dedicated output directory and inspect generated files before moving them into production assets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/nano-banana-2-background-replace)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a fixed AI Hive image model and can save generated image files to a user-selected output directory.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
