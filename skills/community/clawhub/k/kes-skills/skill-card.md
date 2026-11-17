## Description:

KES Skills is a KingbaseES V8/V9 skill pack that helps agents answer questions and provide guidance across installation, deployment, SQL, drivers, frameworks, operations, security, performance tuning, migration, troubleshooting, application development, vector extensions, and MCP server usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wklxd](https://clawhub.ai/user/wklxd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, database administrators, and operators use this skill pack to get KingbaseES guidance, examples, commands, configuration snippets, troubleshooting workflows, and application integration patterns across the database lifecycle.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes high-impact database deployment and operations runbooks involving Docker, firewall or SELinux changes, scheduled jobs, password handling, trust authentication, remote installation, and maintenance actions.

Mitigation: Review commands before use, replace examples with pinned downloads, least-privilege containers, locked service accounts, scoped firewall rules, protected secrets, explicit backups, and confirmation gates for destructive maintenance.

Risk: Generated database administration guidance can be incorrect or unsuitable for a specific production environment.

Mitigation: Validate recommendations against local KingbaseES versions, topology, backup policy, security requirements, and change-management procedures before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wklxd/skills/kes-skills)
- [KES Skills overview](artifact/README.en.md)
- [KES Skills manifest](artifact/SKILL.md)
- [KES Core quick start](artifact/kes-core/quick-start.md)
- [SQL optimization patterns](artifact/kes-sql-tuning/ref/sql-optimization-patterns.md)
- [Security authentication reference](artifact/kes-security/ref/security-auth.md)
- [Migration best practices](artifact/kes-migration/ref/migration-best-practice.md)
- [MCP tools reference](artifact/kes-mcp/ref/tools-reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with SQL, code, shell command, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include step-by-step operational guidance, diagnostic checklists, and database administration examples.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
