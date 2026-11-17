## Description:

Use this skill when the user wants to query, analyze, or explore data in Alibaba Cloud ODPS (MaxCompute / 阿里云大数据计算服务).

This skill is ready for commercial/non-commercial use.

## Publisher:

[guilongzh](https://clawhub.ai/user/guilongzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data analysts use this skill to list ODPS tables, inspect schemas, run MaxCompute SQL queries, and summarize query results for data exploration workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run unrestricted SQL against ODPS using cloud credentials.

Mitigation: Use a dedicated read-only ODPS/RAM identity with minimal project and table access, and review SQL before execution.

Risk: The skill may default to plaintext HTTP MaxCompute endpoints.

Mitigation: Set the endpoint explicitly to an HTTPS endpoint before use.

Risk: The helper can load credentials from local .env files.

Mitigation: Run it only from trusted project directories and avoid directories that contain unrelated .env files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guilongzh/skills/odps-sql)
- [ODPS SQL reference guide](artifact/references/odps_sql_guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline SQL and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute ODPS helper commands that return table lists, schema details, and SQL query results.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
