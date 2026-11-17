## Description:

Health Data Analyzer helps agents query and analyze sleep, exercise, recovery, and related health metrics from a healthdata MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianchuanjun64-afk](https://clawhub.ai/user/tianchuanjun64-afk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect health database tables, run healthdata MCP queries, and summarize sleep quality, exercise load, recovery state, trends, and data quality signals. It is intended for health-data analysis workflows where the user controls or trusts the connected MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can query sensitive health and profile data from the configured healthdata MCP server.

Mitigation: Use it only in trusted local environments and limit queries to the minimum tables, date ranges, and fields needed for the user's request.

Risk: The included workflows support user_info and complete-profile queries that may expose personal profile and device-source data.

Mitigation: Avoid profile-wide queries unless explicitly necessary and authorized by the data owner.

Risk: The status script writes a fixed temporary file and may automatically change script permissions.

Mitigation: Do not run the status script with elevated privileges until the temporary-file and chmod behavior are reviewed and corrected.

## Reference(s):

- [Health Data Analyzer ClawHub Release](https://clawhub.ai/tianchuanjun64-afk/skills/health-data-analyzer)
- [Database Schema](references/database-schema.md)
- [Query Patterns](references/query-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include health metric summaries, trend observations, MCP command examples, and personalized recommendations based on queried data.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
