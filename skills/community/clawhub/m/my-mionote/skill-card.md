## Description:

只读查询用户在 Meet妙记（MioNote）中的会议纪要、AI 摘要、笔记和转写，帮助提炼行动项、决策并引用原话。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mionote](https://clawhub.ai/user/mionote)

### License/Terms of Use:

Apache 2.0

## Use Case:

Meet妙记用户可用此技能按时间、分组或标题查找自己的会议，并读取纪要、摘要和转写。助手可据此整理会议要点、行动项与决策，或按说话人和时间引用原话。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Retrieved meeting notes and transcripts enter the conversation and may be processed by the user's AI provider.

Mitigation: Use the skill only for meetings the user is comfortable having that provider process.

Risk: The API key is stored locally, and logging out removes the saved key without revoking it.

Mitigation: Enter the key through the hidden terminal prompt, protect the saved credential, and revoke or reset the key in the MioNote app if needed.

Risk: Transcript exports may contain sensitive meeting content.

Mitigation: Remove sensitive transcript exports when finished.

## Reference(s):

- [Meet妙记产品网站](https://www.mionote.com.cn)
- [Meet妙记纪要查询 on ClawHub](https://clawhub.ai/mionote/skills/my-mionote)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese natural-language answers, meeting summaries, lists, and transcript excerpts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content follows the requested meetings and fields; quoted excerpts can include speaker names and timestamps when available.]

## Skill Version(s):

2.0.1 (source: server-resolved release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
