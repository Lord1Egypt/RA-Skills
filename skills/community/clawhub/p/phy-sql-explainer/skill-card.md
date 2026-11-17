## Description:

Analyzes PostgreSQL, MySQL, and SQLite execution plans to identify bottlenecks, stale statistics, missing indexes, N+1 patterns, and practical fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database engineers use this skill to analyze pasted SQL queries and execution plans, then receive a concise diagnosis with prioritized index, statistics, configuration, and rewrite recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to run live database analysis, including EXPLAIN ANALYZE, without clear confirmation or safety limits.

Mitigation: Prefer pasted execution plans; before live analysis, confirm the target database, permissions, statement safety, and resource limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-sql-explainer)
- [Publisher profile](https://clawhub.ai/user/phy041)
- [Canlah AI homepage](https://canlah.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown report with SQL code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include prioritized SQL index, ANALYZE, configuration, and query rewrite suggestions.]

## Skill Version(s):

1.0.3 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
