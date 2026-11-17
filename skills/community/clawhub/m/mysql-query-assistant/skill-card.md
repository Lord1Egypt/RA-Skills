## Description:

Translates natural-language analytics requests into MySQL queries, inspects live database schema and column comments, executes read-only SQL, and validates query correctness against real results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nocb](https://clawhub.ai/user/nocb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to convert ad hoc business questions into validated MySQL queries against databases provided through environment variables. It supports cautious database workflows by inspecting schema before query generation, executing only read-only SQL, and producing preview SELECT statements for restricted write requests without executing writes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security verdict is suspicious because the database read-only safety guard is incomplete.

Mitigation: Install only with a dedicated least-privilege MySQL account limited to SELECT and metadata access, with FILE, write, admin, routine execution, and privilege-management permissions revoked.

Risk: The skill connects to live databases and can expose sensitive data through query results.

Mitigation: Use bounded queries, keep result samples small, and verify TLS behavior before using the skill against remote or sensitive databases.

Risk: Generated SQL or schema interpretation can be incorrect or misleading.

Mitigation: Review structural validation for tables, columns, joins, filters, grouping, and syntax, then compare returned rows and aggregates with the user's intent before presenting results.

## Reference(s):

- [Connection and Safety](artifact/references/connection-and-safety.md)
- [ClawHub Skill Page](https://clawhub.ai/nocb/skills/mysql-query-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown sections with SQL code blocks, validation notes, sample results, result summaries, and caveats.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include compact JSON output from bundled schema and read-query scripts; sample rows are bounded by default.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
