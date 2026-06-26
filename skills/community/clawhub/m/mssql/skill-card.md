## Description: <br>
Execute SQL Server queries and export results as delimiter-separated text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xvespertine](https://clawhub.ai/user/0xvespertine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and reporting agents use this skill to query Microsoft SQL Server, validate BI or reporting numbers, manage scoped data tasks, and export result sets for downstream analysis or charts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad SQL Server execution authority through stored credentials. <br>
Mitigation: Use a least-privileged database account, preferably read-only for reporting workflows, and limit access to only the databases and schemas required. <br>
Risk: The helper does not add built-in guardrails for insert, update, delete, schema, or administrative queries. <br>
Mitigation: Manually approve any write, schema, or administrative query before execution. <br>
Risk: Database credentials are loaded from a local credential file. <br>
Mitigation: Protect the credential file, restrict filesystem access, and avoid exposing credentials in responses or logs. <br>
Risk: Delimiter-separated output can be malformed when data contains embedded delimiters, quotes, or newlines. <br>
Mitigation: Choose a delimiter that does not appear in the result data or post-process the output before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xvespertine/mssql) <br>
- [DB_MAP.example.md](references/DB_MAP.example.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Delimiter-separated text output, Markdown guidance, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Query results are delimiter-separated text, not RFC 4180 CSV; fields are not quoted or escaped.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
