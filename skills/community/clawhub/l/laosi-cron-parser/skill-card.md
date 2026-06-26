## Description: <br>
Cron解析 - 解析cron表达式，翻译为自然语言，计算下次执行时间，支持标准和扩展语法 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and automation operators use this skill to understand, validate, describe, and generate cron schedules for task scheduling, monitoring, and scripted automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The broad trigger word "cron" may activate this skill more often than intended. <br>
Mitigation: Use explicit requests such as "parse this cron expression" or "explain this schedule" when invoking the skill. <br>
Risk: Cron parsing and next-run examples may be misleading if the user expects a different cron dialect, timezone, or scheduler-specific extension. <br>
Mitigation: Confirm the target scheduler syntax and timezone before using generated expressions in production automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/534422530/laosi-cron-parser) <br>
- [Publisher profile](https://clawhub.ai/user/534422530) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with cron expressions, natural-language descriptions, Python code examples, and schedule guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated cron templates and next-run timestamps based on local datetime calculations.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
