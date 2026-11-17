## Description:

Lucid Skill lets agents connect CSV, Excel, MySQL, and PostgreSQL sources, discover semantics and relationships, and answer data questions with read-only SQL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenkang-xie](https://clawhub.ai/user/wenkang-xie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data-focused teams use Lucid Skill to connect local files or supported databases, inspect schemas and relationships, create semantic definitions, and run read-only SQL-backed analysis through a CLI or MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Read-only and connected-data boundaries may be insufficient for sensitive databases and files.

Mitigation: Use least-privilege, read-only database accounts and non-production data where possible.

Risk: Secrets and local catalog data may be exposed through shell history or retained in the data directory.

Mitigation: Avoid passing secrets through shell commands, set LUCID_DATA_DIR to a controlled directory, and delete local catalogs when no longer needed.

Risk: Untrusted file paths or Excel sheet names may create unsafe local data handling conditions.

Mitigation: Connect only trusted files and sheet names, and review connected source metadata before querying.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wenkang-xie/skills/lucid-skill)
- [CLI Command Reference](references/commands.md)
- [update-semantic JSON Schema](references/json-schema.md)
- [Workflow Guides](references/workflow.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [JSON by default, with optional Markdown or CSV query results and inline SQL or shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only SQL execution is intended; outputs may include schema details, sample values, join hints, semantic definitions, and truncated query results.]

## Skill Version(s):

2.0.0 (source: server release metadata and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
