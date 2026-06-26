## Description: <br>
Hologres Query Optimizer helps agents analyze Hologres SQL execution plans, interpret EXPLAIN and EXPLAIN ANALYZE output, and propose query performance optimizations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wenbingyu](https://clawhub.ai/user/wenbingyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database engineers use this skill to diagnose slow Hologres SQL, read execution plan metrics, and choose targeted fixes such as statistics refreshes, distribution-key changes, indexing, join-order tuning, or GUC adjustments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes example database commands that can execute queries or change Hologres tuning settings. <br>
Mitigation: Verify hologres-cli before use, use least-privilege database credentials, and require explicit review before running EXPLAIN ANALYZE, ANALYZE, set_table_property, or persistent hologres guc set commands, especially on production databases. <br>
Risk: Query-tuning recommendations can be incorrect or unsuitable for a specific workload. <br>
Mitigation: Review proposed changes against the actual execution plan, test in a safe environment when possible, and apply production changes through the normal database change process. <br>


## Reference(s): <br>
- [Hologres Query Optimizer on ClawHub](https://clawhub.ai/wenbingyu/hologres-query-optimizer) <br>
- [Hologres Query Operators Reference](references/operators.md) <br>
- [Hologres Query Optimization Patterns](references/optimization-patterns.md) <br>
- [Hologres GUC Parameters for Query Tuning](references/guc-parameters.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with SQL and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces recommendations and example commands for human review before execution.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata and VERSION file; artifact package.json reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
