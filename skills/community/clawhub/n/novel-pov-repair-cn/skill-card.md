## Description:

输入单个章节、场景或短文及指定视角人物，诊断具体叙事视角越界，逐处给出位置、越界原因和不改变情节的修订片段。适用于第三人称限知或第一人称初稿校对；缺少文本或视角人物时，仅列实际缺项并停止，不臆测全文，也不新增角色知情、动作或台词。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

中文小说作者和编辑可用它检查第一人称或第三人称限知文本中的视角越界，了解越界原因，并获得保留情节、动作、台词与人物知情范围的最小修订片段。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 文档中的安装命令未固定版本；安全审查还指出安装说明与该技能的编辑用途可能不一致。

Mitigation: 安装前核实包的身份，检查发布内容和安装行为；如支持，请固定到预期版本。

## Reference(s):

- [Project page](https://github.com/xxjrq/novel-pov-repair-cn)
- [Story Skills: scene-craft](https://github.com/danjdewhurst/story-skills/blob/main/skills/scene-craft/SKILL.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [中文 Markdown，包含判定、视角越界诊断表、最小修订片段和修订原则；缺少必需输入时列出缺项。]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [每次处理一批用户提供的文本；表格超过 100 行或材料无法完整处理时要求分批。缺少场景文本或视角人物时停止诊断。]

## Skill Version(s):

1.0.1 (source: manifest.yaml, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
