## Description:

自动填写 iHub 测试农场平台指定日期的日报，支持自定义账号密码和 Markdown 格式内容输入。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaqima2024](https://clawhub.ai/user/shaqima2024)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and team members who maintain iHub daily reports use this skill to navigate the iHub Test Farm workflow, locate a named user's dated report entry, fill Markdown content, and submit the update.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles real iHub login passwords and may expose them through command-line use, terminal logs, or returned output.

Mitigation: Use a protected password prompt or delegated authentication, avoid passing passwords on the command line, do not run it where terminal output is logged, and never print or return the password.

Risk: The skill can automatically submit daily-report records to an external iHub system.

Mitigation: Use it only for the intended iHub daily-report workflow and require confirmation of the account, date, target person, and report content before final submission.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shaqima2024/skills/ihub-daily-report)
- [ClawHub publisher profile](https://clawhub.ai/user/shaqima2024)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown instructions with JavaScript automation status as log text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a name, username, password, report content, and optional target date to drive the daily-report workflow.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
