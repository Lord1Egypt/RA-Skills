## Description:

飞书考勤打卡：查询自己的考勤打卡记录

This skill is ready for commercial/non-commercial use.

## Publisher:

[gu2003li](https://clawhub.ai/user/gu2003li)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and authorized Lark/Feishu users use this skill to query their own attendance punch records through lark-cli.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use an existing lark-cli session to query Feishu/Lark attendance records.

Mitigation: Confirm lark-cli is authenticated to the intended tenant and account, and keep queries limited to records the user is authorized to view.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gu2003li/skills/lark-attendance)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON parameter snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authenticated lark-cli session with attendance:task:readonly scope; employee_type is fixed to employee_no and user_ids is fixed to an empty array.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
