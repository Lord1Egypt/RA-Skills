## Description:

输入最多30名角色的实名与已确认别名、说话人到称呼对象的批准关系规则，以及最多100条带章节锚点的称呼片段，输出姓名变体与归属表、错称或歧义位置和逐处替换建议，适用于中文小说定稿前核对；缺少别名归属、说话人或对象时标为待确认，同名人物分开处理，不作全局替换。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT No Attribution (MIT-0)

## Use Case:

中文小说作者和编辑可用此技能按角色表与已批准的称呼规则核对定稿，查看带章节锚点的错称、歧义和逐处建议，并在确认前保留原文。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A suggested correction or incorrect-address finding could be mistaken for a definitive editorial decision, especially when approved forms or identity details are incomplete.

Mitigation: Review the source and each anchored finding; confirm character IDs, approved address rules, and every proposed change yourself.

## Reference(s):

- [Story-skills character-management (domain reference)](https://github.com/danjdewhurst/story-skills/blob/main/skills/character-management/SKILL.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown tables with anchored findings and per-location suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Checks up to 30 characters and 100 address mentions; unresolved identity data is marked for confirmation; no global replacements.]

## Skill Version(s):

1.0.0 (source: release evidence and manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
