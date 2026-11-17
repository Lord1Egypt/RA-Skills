## Description:

Automates daily technology news retrieval from Jiqizhixin, pushes the results to Feishu, and saves them to GetNote.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bqcldz](https://clawhub.ai/user/bqcldz)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to configure credentials, fetch the latest Jiqizhixin technology headlines, send them through Feishu, save them to GetNote, and optionally schedule a daily push.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential checks in the skill documentation may print full secrets to the terminal.

Mitigation: Use presence-only checks for required environment variables and avoid echoing token or API key values.

Risk: The recurring cron setup may run with broad privileges or write sensitive logs to a shared location.

Mitigation: Run scheduled jobs as an unprivileged user, write logs to a private user-owned file, and keep a clear cron removal command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bqcldz/skills/jqzx-news-push)
- [Publisher profile](https://clawhub.ai/user/bqcldz)
- [Jiqizhixin MCP/RSS service](https://mcp.applications.jiqizhixin.com/)
- [GetNote OpenAPI](https://www.biji.com/openapi)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided Jiqizhixin, Feishu, and GetNote credentials.]

## Skill Version(s):

1.0.0 (source: package.json and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
