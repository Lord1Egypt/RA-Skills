## Description: <br>
查询用户自己的飞书/Lark 考勤打卡记录。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gu2003li](https://clawhub.ai/user/gu2003li) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and authorized Feishu/Lark users use this skill to query their own attendance punch records through lark-cli. The skill guides the agent to inspect the attendance schema before calling the native API and to use fixed attendance query parameters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Attendance records may contain sensitive workplace data. <br>
Mitigation: Use only with an authenticated Feishu/Lark account that is authorized to view the requested records, and limit disclosure of returned attendance data. <br>
Risk: Incorrect attendance API parameters could query unintended data or fail unexpectedly. <br>
Mitigation: Follow the fixed employee_type and empty user_ids rules, and inspect lark-cli schema output before calling the attendance API. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gu2003li/lark-attendance) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON parameter examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses lark-cli and fixed query parameters: employee_type is employee_no and user_ids is an empty array.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
