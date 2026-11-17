## Description:

Execute SQL Server queries and export results as delimiter-separated text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xvespertine](https://clawhub.ai/user/0xvespertine)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data analysts, and agents use this skill to query Microsoft SQL Server, validate reporting numbers, manage data when authorized, and prepare database result sets for analysis or charts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run unrestricted SQL against the configured SQL Server according to the database user's grants.

Mitigation: Use a least-privilege SQL Server account, preferably read-only unless writes are required, and confirm insert, update, delete, schema, or administrative queries before execution.

Risk: The skill loads credentials and the sqlcmd binary from the local environment.

Mitigation: Install only in a trusted environment, restrict the credential file, trust the selected sqlcmd binary, and never expose credentials in responses.

Risk: Delimiter-separated output is not quoted or escaped, so embedded delimiters, quotes, or newlines can corrupt downstream parsing.

Mitigation: Choose a delimiter that does not appear in the data or post-process the output before using it in automated analysis.

## Reference(s):

- [DB_MAP.example.md](references/DB_MAP.example.md)
- [ClawHub MSSQL skill page](https://clawhub.ai/0xvespertine/skills/mssql)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration]

**Output Format:** [Delimiter-separated text written to stdout or a .dsv file, with Markdown guidance for command usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output is not RFC 4180 CSV; fields are not quoted or escaped.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
