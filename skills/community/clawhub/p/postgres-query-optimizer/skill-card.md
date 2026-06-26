## Description: <br>
Analyzes slow PostgreSQL queries and EXPLAIN ANALYZE output to identify bottlenecks and recommend indexes, query rewrites, and configuration tuning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, database administrators, and backend engineers use this skill to diagnose slow PostgreSQL queries, interpret query plans, and plan performance improvements before applying database changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SQL indexes, query rewrites, or configuration advice can change database behavior, add write overhead, or cause plan regressions if applied directly in production. <br>
Mitigation: Treat outputs as recommendations, have a DBA review them, test on staging or during a maintenance window, benchmark before and after, and keep a rollback path. <br>
Risk: EXPLAIN ANALYZE executes the query, which can be costly and may modify data for write queries. <br>
Mitigation: Use care with write queries, prefer non-production data for analysis, or use safer EXPLAIN-only and transaction rollback patterns when appropriate. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with SQL code blocks and plain-language analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include query analysis, EXPLAIN commands, index recommendations, query rewrites, configuration suggestions, estimated impact, and warnings.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
