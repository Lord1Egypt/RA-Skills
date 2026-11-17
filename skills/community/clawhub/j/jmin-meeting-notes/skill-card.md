## Description:

会议记录智能整理工具。输入会议要点或文字记录，自动生成结构化会议纪要、待办事项、决策记录。适用于职场人士、会议组织者、项目管理者。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jmin1113](https://clawhub.ai/user/jmin1113)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, meeting organizers, and project managers use this skill to turn raw meeting notes, transcripts, or spoken bullet points into structured minutes with decisions, action items, owners, and follow-up agenda items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting notes can contain client names, private employee details, credentials, financial figures, regulated data, or other sensitive material.

Mitigation: Redact sensitive material before sharing meeting content with the agent unless that sharing is approved.

Risk: Generated minutes, decisions, owners, deadlines, or follow-up agenda items may be incomplete or inaccurate if the input notes are ambiguous.

Mitigation: Review the generated minutes against the source meeting record before circulating or assigning follow-up work.

## Reference(s):

- [Meeting note templates](references/templates.md)
- [ClawHub skill page](https://clawhub.ai/jmin1113/skills/jmin-meeting-notes)
- [Publisher profile](https://clawhub.ai/user/jmin1113)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown meeting minutes with tables and structured sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include decisions, action items, responsible owners, deadlines, risks, and next-meeting agenda items.]

## Skill Version(s):

1.0.0 (source: release evidence and README, released 2026-03-31)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
