## Description:

将实习中的零散记录、聊天片段和任务笔记整理成可直接粘贴的中文日报或进展汇报。适用于写日报、整理今天任务、发给导师或 leader 的进展同步，以及填写“计划阶段、汇报阶段、进展状态、进展情况、问题及原因”等固定字段。

This skill is ready for commercial/non-commercial use.

## Publisher:

[npccxx](https://clawhub.ai/user/npccxx)

### License/Terms of Use:

MIT-0

## Use Case:

Interns, employees, and students use this skill to turn scattered notes, chat excerpts, task lists, and learning records into Chinese daily reports or progress updates ready for mentors, leaders, or fixed-field reporting systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Internship notes may include sensitive company, project, or personal information that could be sent to the runtime model configured in the user's environment.

Mitigation: Remove confidential identifiers and only submit details suitable for the configured runtime model and workplace policy.

Risk: Incomplete notes can produce reports with missing or misleading context.

Mitigation: Review the generated report before sharing it and fill any fields marked 待补充 with verified facts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/npccxx/skills/internship-daily-reflection)
- [Examples](references/examples.md)
- [Internship Daily Report Template](assets/template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Chinese Markdown report or structured fixed-field text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask follow-up questions when key report fields are missing; otherwise marks missing facts as 待补充 rather than inventing details.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
