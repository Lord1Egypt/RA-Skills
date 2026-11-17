## Description:

依据用户提供的小说或剧本，由 AI 创作包含人物、场景、动作、对白、镜头和时长的中文分镜。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

面向小说作者、编剧及内容创作者，将提供的故事文本整理为便于拍摄和审阅的中文分镜。用户可指定时长、画幅或风格，并检查原文依据及待确认信息。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 分镜可能误述原文或把未说明的动机写成事实；结构和时长检查不能判断改编是否忠于原作。

Mitigation: 对照原文核对人物、事件与原文锚点，并将不确定的信息标为待确认。

Risk: 输出文件可能与目录中已有的 storyboard 文件冲突。

Mitigation: 为本次输出选择一个新的目录。

## Reference(s):

- [ClawHub release page](https://clawhub.ai/xxjrq/skills/novel-script-storyboard)
- [分镜 JSON 字段](references/schema.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [中文分镜文本、Markdown 分镜表和结构化 JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [包含人物、场景、镜头、对白、时长及原文锚点；未说明的信息和创作补充可单独标注。]

## Skill Version(s):

1.0.2 (source: release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
