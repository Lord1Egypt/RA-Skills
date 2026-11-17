## Description:

根据中文连载小说的上几章正文或摘要及下一章目标，生成120至250字读者前情提要和作者续写记忆卡，保留人物当前状态、事件因果与未解线索；已知事实、衔接建议和待确认信息分开，缺少材料或目标时请求补充。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

中文连载小说作者和编辑可用此技能整理已提供的章节正文或摘要，生成供读者快速回顾的前情提要，以及帮助作者承接下一章的记忆卡。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented npx installation command can execute downloaded code without pinning a version.

Mitigation: Use a reviewed package directory or a trusted installer version, as advised by the security guidance.

Risk: Chapter material may contain text the user does not want to share with an agent.

Mitigation: Provide only chapter material the user is comfortable sharing with the agent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xxjrq/skills/novel-serial-recap-cn)
- [Story Long Write use-case reference](https://github.com/zenstory-ai/oh-story-claudecode/blob/main/skills/story-long-write/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A 120–250-character Chinese reader recap and a structured author memory card; missing inputs are requested, and established facts are separated from continuation suggestions.]

## Skill Version(s):

1.0.1 (source: manifest.yaml and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
