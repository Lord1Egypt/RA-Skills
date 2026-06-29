## Description: <br>
Analyzes PostgreSQL slow queries, execution plans, schemas, and workload statistics to recommend indexes, query rewrites, and tuning changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-gaoqian](https://clawhub.ai/user/ai-gaoqian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, database administrators, and performance engineers use this skill to turn PostgreSQL query plans, slow query logs, schemas, and workload statistics into prioritized tuning recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SQL, schema, and performance data pasted into the skill can contain sensitive operational information. <br>
Mitigation: Share only data approved for the agent environment and redact secrets, customer data, and sensitive identifiers before use. <br>
Risk: Generated index, query rewrite, or configuration advice could affect production database performance or behavior. <br>
Mitigation: Review all recommendations, test them in a non-production environment, and apply changes through normal database change controls. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with SQL snippets, diagnostic notes, and configuration recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include proposed CREATE INDEX statements, query rewrites, estimated performance impact, and PostgreSQL configuration changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
