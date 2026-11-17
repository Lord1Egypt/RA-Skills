## Description:

Automates heterogeneous database migration to KaiwuDB / KWDB through the KDTS REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kwdb](https://clawhub.ai/user/kwdb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database engineers use this skill to plan and execute migrations from supported relational, time-series, file, and NoSQL sources into KaiwuDB / KWDB. It guides parameter collection, connection testing, schema and data migration, task monitoring, and error handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Database credentials may be exposed in chat or sent to an untrusted KDTS server.

Mitigation: Use HTTPS to a trusted KDTS server, avoid pasting production passwords or tokens into chat, and prefer secret-manager or environment references.

Risk: Migration workflows can perform schema-changing or data-changing operations.

Mitigation: Use least-privileged database accounts and require explicit human approval immediately before DDL execution or data migration execution.

Risk: Terminating a migration task can leave database state inconsistent.

Mitigation: Require explicit human approval before task termination and review database-impacting workflows before installation.

## Reference(s):

- [KWDB Data Migration Skill Page](https://clawhub.ai/kwdb/skills/kwdb-data-migration)
- [KDTS API Reference](references/api-reference.md)
- [Configuration Templates](references/config-templates.md)
- [KaiwuDB DDL Syntax Reference](references/ddl-syntax.md)
- [Error Code Reference](references/error-codes.md)
- [Supported Source Types](references/source-types.md)
- [Type Mapping Reference](references/type-mapping.md)
- [KWDB Data Migration Scripts](scripts/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code, JSON configuration examples, shell commands, and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual English and Chinese responses; migration actions require user-supplied connection details and KDTS availability.]

## Skill Version(s):

1.2.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
