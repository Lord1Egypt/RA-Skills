## Description: <br>
Provides PostgreSQL query-performance analysis and optimization guidance for slow query logs, EXPLAIN ANALYZE plans, indexing, query rewrites, table design, statistics, and configuration tuning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-gaoqian](https://clawhub.ai/user/ai-gaoqian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, DBAs, and operations engineers use this skill to diagnose PostgreSQL query and instance performance issues and receive concrete optimization advice, including SQL DDL/DML examples and configuration recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Query logs, execution plans, and schema details can contain sensitive business information. <br>
Mitigation: Review and redact sensitive inputs before sharing them with the agent. <br>
Risk: Generated SQL or tuning advice could affect production database behavior if applied without review. <br>
Mitigation: Have a qualified developer or DBA review recommendations and test changes before running them on production databases. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ai-gaoqian/postgres-optimizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with SQL and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include risk-labeled SQL recommendations, index DDL, query rewrites, performance estimates, and PostgreSQL configuration guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
