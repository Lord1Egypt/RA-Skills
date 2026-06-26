## Description: <br>
自然语言转 SQL 查询助手将用户的自然语言描述转换为 SQL, connects to local or remote MySQL databases, executes SELECT/INSERT/UPDATE/DELETE and transaction workflows, and returns table, CSV, or JSON results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyesky](https://clawhub.ai/user/cyesky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and database operators use this skill to translate natural-language database requests into MySQL statements, inspect schemas, execute reads and writes, and present results while masking credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute real SQL reads and writes against MySQL databases. <br>
Mitigation: Use a test database or least-privileged database account and review the exact SQL before execution. <br>
Risk: Write, delete, schema-change, and transaction operations can alter or destroy data. <br>
Mitigation: Require explicit approval for every INSERT, UPDATE, DELETE, DROP, TRUNCATE, schema change, or transaction before running it. <br>
Risk: Database credentials may be exposed when passed through command-line flags or shown in assistant output. <br>
Mitigation: Avoid root and production credentials, avoid command-line password flags when possible, and mask passwords in all displayed connection information. <br>


## Reference(s): <br>
- [NL2SQL Reference Guide](artifact/references/guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/cyesky/nl2sql) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with SQL code blocks, shell commands, and table, CSV, or JSON query results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated SQL should be shown before execution, database passwords should be masked, and large result sets may be summarized.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
