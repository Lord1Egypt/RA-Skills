## Description:

Phy Db Index Advisor statically scans ORM query patterns and existing index definitions to recommend missing database indexes before they become production bottlenecks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database engineers use this skill to scan application source code for repeated WHERE, ORDER BY, and JOIN patterns, then review generated index SQL and ORM migration snippets before staging or production rollout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local project source files to analyze ORM query and migration patterns.

Mitigation: Run it only on codebases you are allowed to inspect and handle scan results under the same controls as the source code.

Risk: Suggested indexes can affect database locks, storage use, write performance, and production query behavior.

Mitigation: Have a database owner review recommendations, test them in staging, and plan production rollout carefully.

Risk: Static analysis can miss dynamic filters or recommend a single-column index where a composite index is more appropriate.

Mitigation: Review query plans with runtime evidence such as EXPLAIN ANALYZE and tune thresholds before acting on findings.

## Reference(s):

- [Canlah AI homepage](https://canlah.ai)
- [ClawHub skill listing](https://clawhub.ai/phy041/skills/phy-db-index-advisor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown report with SQL and ORM migration snippets; optional JSON scanner output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can report CI pass or fail status when critical missing indexes are detected.]

## Skill Version(s):

1.0.3 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
