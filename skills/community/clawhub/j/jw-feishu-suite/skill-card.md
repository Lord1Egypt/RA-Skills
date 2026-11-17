## Description:

Feishu Suite helps agents manage Feishu messages, documents, calendars, tasks, and bitable records for workplace collaboration and workflow automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a85012712](https://clawhub.ai/user/a85012712)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, operators, and developers use this skill to ask an agent to send Feishu messages, create or update documents, manage calendar events and tasks, and work with bitable records after user authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad workplace permissions across Feishu messages, documents, calendars, tasks, and bitables.

Mitigation: Install only when those Feishu scopes are intended, and review Feishu authorization prompts carefully before approving access.

Risk: State-changing actions such as message sends, document updates, task changes, calendar updates, and bitable writes can affect shared workplace resources.

Mitigation: Prefer explicit Feishu-prefixed requests for state-changing actions and review confirmation prompts before approving writes or sends.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/a85012712/skills/jw-feishu-suite)
- [ClawHub publisher profile](https://clawhub.ai/user/a85012712)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Configuration]

**Output Format:** [Natural-language guidance and structured Feishu operation requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user authorization for Feishu operations; sensitive operations may require explicit confirmation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
