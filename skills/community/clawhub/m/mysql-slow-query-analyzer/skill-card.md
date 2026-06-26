## Description: <br>
Analyzes MySQL EXPLAIN output and slow query logs to identify query performance bottlenecks and suggest indexes, SQL rewrites, and performance metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenghoo123-png](https://clawhub.ai/user/shenghoo123-png) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, DBAs, and engineering reviewers use this skill to inspect MySQL EXPLAIN output, slow query logs, and SQL snippets before or during performance troubleshooting. It helps prioritize slow queries and produces practical index, rewrite, and metric-based optimization guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Production slow logs, schemas, and SQL literals may contain sensitive customer data, hostnames, or business identifiers. <br>
Mitigation: Redact sensitive values before pasting data into the skill or storing its outputs. <br>
Risk: Index and SQL rewrite recommendations are heuristic and may be incorrect for a specific schema, workload, or MySQL version. <br>
Mitigation: Review suggestions with EXPLAIN or EXPLAIN ANALYZE, test them in a non-production environment, and get DBA review before applying changes. <br>
Risk: The artifact states limitations for stored procedures, triggers, complex multi-statement transactions, and optimality of index advice. <br>
Mitigation: Use the skill as triage guidance for supported single-query cases and rely on database-native diagnostics for unsupported query forms. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shenghoo123-png/mysql-slow-query-analyzer) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown-style analysis reports, human-readable CLI text, and structured Python dictionaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces heuristic query optimization advice for local review; no network upload is indicated by the security evidence.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
