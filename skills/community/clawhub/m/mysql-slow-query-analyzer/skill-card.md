## Description:

Analyzes MySQL EXPLAIN output and slow query logs to identify performance bottlenecks and suggest indexes, SQL rewrites, and query-quality metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenghoo123-png](https://clawhub.ai/user/shenghoo123-png)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, database engineers, and DBAs use this skill to review MySQL queries, EXPLAIN plans, and slow-query log entries before release or during performance troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Index and SQL rewrite recommendations are heuristic and may not be optimal for a production database.

Mitigation: Review recommendations with a DBA and validate them against representative data, EXPLAIN output, and workload behavior before applying changes.

Risk: The parser accepts user-provided SQL, EXPLAIN output, and slow-query log text.

Mitigation: Do not expose the parser as a long-running public service without input validation, size limits, and exception handling.

Risk: The skill's guidance and examples are primarily Chinese-language.

Mitigation: Install only when Chinese-language MySQL performance guidance is acceptable for the target users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shenghoo123-png/skills/mysql-slow-query-analyzer)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown and JSON-style analysis reports with optional CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are heuristic MySQL performance findings and should be reviewed before production database changes.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
