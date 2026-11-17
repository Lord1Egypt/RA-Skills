## Description:

Jira集成技能帮助代理通过 Jira API 创建工单、同步状态并自动化项目管理工作流。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, project managers, and automation operators can use this skill to draft or execute Jira issue creation, status synchronization, and workflow automation through an agent interface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad local read, write, and command capabilities while also being able to modify Jira records.

Mitigation: Use least-privilege Jira credentials, run in a constrained environment, and require explicit confirmation before creating, updating, or transitioning issues.

Risk: API keys or Jira credentials could be exposed through configuration, logs, or agent output.

Mitigation: Store credentials in environment variables or a secret manager, avoid committing secrets, and redact tokens from logs and responses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/jira-integration-skill)
- [Publisher profile](https://clawhub.ai/user/thcjp)
- [Skill homepage](https://skillhub.cn/skill/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown text with JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe Jira API request parameters, operation results, configuration steps, and error handling guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
