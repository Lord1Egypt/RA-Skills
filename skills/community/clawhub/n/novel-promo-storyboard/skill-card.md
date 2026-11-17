## Description:

依据用户实际提供的小说或梗概，由当前 AI 完成推广创意与分镜。整理用户意图、标题、人物场景、口播/镜头时间线、声音提示和原文锚点；辅助脚本只校验排版，不会生成推广内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT No Attribution (MIT-0)

## Use Case:

面向需要推广小说的创作者，帮助 AI 根据用户提供的原文或梗概制作推广脚本与分镜，并把原文依据、创意补充和待确认信息分开。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A storyboard may misstate the source; the formatting helper does not check factual fidelity.

Mitigation: Review source anchors, narration, and captions against the supplied text before publishing.

Risk: The workflow requires sharing source material with the AI.

Mitigation: Provide only material you are authorized to share.

## Reference(s):

- [Skill output schema](artifact/references/output-schema.md)
- [ClawHub skill page](https://clawhub.ai/xxjrq/skills/novel-promo-storyboard)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown]

**Output Format:** [Chinese promotional scripts and storyboards; optionally a structured JSON package rendered as Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include titles, character and scene notes, timed narration and shots, sound cues, source anchors, and review gaps. The helper validates structure and layout, not fidelity to the source.]

## Skill Version(s):

1.0.2 (source: package.json, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
