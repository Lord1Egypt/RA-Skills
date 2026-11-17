## Description:

Queries China Railway ticket and schedule information through the mcporter CLI and a user-configured 12306 MCP server, with helpers for station-code lookup, time-window filtering, train-type filtering, and result sorting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lancenas](https://clawhub.ai/user/lancenas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and rail-travel users use this skill to query China Railway schedules, ticket availability, and station codes from an agent workflow through mcporter and a configured 12306 MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The global mcporter npm install step can introduce supply-chain risk if the package changes or is compromised.

Mitigation: Use a trusted or pinned mcporter version, or install a reviewed local copy before running the helper scripts.

Risk: Queries rely on the user's configured 12306 MCP server and live railway data.

Mitigation: Use a trusted MCP server configuration and verify important ticket availability before making travel decisions.

## Reference(s):

- [Query Examples](artifact/references/query-examples.md)
- [Station Codes](artifact/references/station-codes.md)
- [ClawHub Skill Page](https://clawhub.ai/lancenas/skills/mcporter-railway-query)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline bash commands; helper scripts return text query results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only ticket, schedule, and station-code queries through mcporter; results depend on the configured 12306 MCP server.]

## Skill Version(s):

1.1.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
