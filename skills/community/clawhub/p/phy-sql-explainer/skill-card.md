## Description: <br>
Analyzes PostgreSQL, MySQL, or SQLite EXPLAIN output to identify SQL performance bottlenecks and recommend indexes, statistics updates, and query rewrites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database engineers use this skill to interpret slow-query plans and produce prioritized SQL tuning guidance for PostgreSQL, MySQL, or SQLite. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may run or suggest live database analysis commands without enough safety limits. <br>
Mitigation: Prefer pasted EXPLAIN output, confirm the exact database target, use read-only or sandbox access, avoid production when possible, and review any EXPLAIN ANALYZE, ANALYZE, or CREATE INDEX command before it runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-sql-explainer) <br>
- [Publisher profile](https://clawhub.ai/user/PHY041) <br>
- [Canlah AI homepage](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Guidance] <br>
**Output Format:** [Markdown report with SQL code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include database-specific SQL statements for EXPLAIN, ANALYZE, CREATE INDEX, and query rewrites.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
