## Description:

Operate the local HiDataLinker desktop database app to inspect saved MySQL, PostgreSQL, SQL Server, and Oracle connections. Use when the user asks to query, inspect, describe, or explain a database that HiDataLinker manages, or mentions 查库, 表结构, SQL, HiDataLinker, or this database client. Do not use for writes, dumps, migrations, or creating connections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[henrybit](https://clawhub.ai/user/henrybit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database users can inspect saved HiDataLinker connections, review database objects and schemas, and run read-only queries to answer questions about managed databases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation steps call for building or copying a local agent binary, and some referenced paths were unresolved during the scan.

Mitigation: Review the installation steps and confirm the expected binary paths before running them.

## Reference(s):

- [HiDataLinker DB skill on ClawHub](https://clawhub.ai/henrybit/skills/hidatalinker-db)
- [HiDataLinker agent tools](references/tools.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Markdown or plain text containing database metadata, read-only query results, and explanations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only; query results are capped at 5,000 rows and table previews at 1,000 rows.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
