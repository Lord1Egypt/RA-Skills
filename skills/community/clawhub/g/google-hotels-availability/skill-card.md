## Description:

Check day-by-day Google Hotels availability (the booking calendar) for a known listing over a date window.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stayingapi](https://clawhub.ai/user/stayingapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check whether a known Google Hotels listing is available across specific dates, including minimum-night and check-in/check-out constraints returned by StayingAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends hotel listing IDs or URLs, requested dates, and a StayingAPI credential to StayingAPI.

Mitigation: Use it only when that third-party API use is acceptable, prefer a sandbox key for evaluation, and store live keys with the normal secret-handling method for the agent runtime or shell.

## Reference(s):

- [StayingAPI homepage](https://stayingapi.com)
- [StayingAPI documentation](https://stayingapi.com/docs)
- [StayingAPI OpenAPI contract](https://api.stayingapi.com/openapi.json)
- [StayingAPI MCP server](https://mcp.stayingapi.com/mcp)
- [Authentication setup](references/auth-setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API request details and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include day-by-day availability summaries, minimum-night constraints, polling guidance for async jobs, and credential setup steps.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
