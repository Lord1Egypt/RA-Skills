## Description:

通用型图像Prompt生成器。输入主题描述，AI自主分析主体特征、决定艺术风格、推荐配色构图，输出结构化Prompt。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fslong520](https://clawhub.ai/user/fslong520)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to turn an image concept, illustration request, poster theme, or visual design brief into a structured prompt. It is especially oriented toward AI image generation workflows that need clear style, composition, lighting, aspect-ratio, and negative-prompt guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests Write and Edit access even though server security evidence says it mainly generates prompt text.

Mitigation: Review before installing and run it only in workspaces where accidental file changes would be acceptable, or remove/tightly scope file-editing permissions before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fslong520/skills/imgmuse)
- [图片姬 - 参考文档](artifact/reference.md)
- [优秀prompt示例](artifact/examples.md)
- [高中信息科技可视化专家](artifact/知识可视化专家.md)
- [智国-创玩2026年4月C++月赛宣传插图 Prompt](artifact/assets/智国创玩C++月赛宣传图-prompt.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown structured prompt with optional JSON structure]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs structured image-prompt dimensions; the skill text says it does not output a plain text or English copy-ready version by default.]

## Skill Version(s):

2.5.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
