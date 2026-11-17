## Description:

Hologres slow query log analysis and diagnosis skill for analyzing slow queries, failed queries, query performance, and log management in Alibaba Cloud Hologres.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenbingyu](https://clawhub.ai/user/wenbingyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, database administrators, and operations engineers use this skill to diagnose Hologres slow or failed queries, inspect query-log fields, tune logging configuration, and export logs for further analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes guidance that may lead users to grant powerful Hologres permissions or change database-level settings.

Mitigation: Install only for authorized Hologres administrators, prefer read-only or statistics permissions over SUPERUSER, and require explicit approval for privilege or ALTER DATABASE commands.

Risk: The skill describes exporting query logs, which may expose sensitive query text, account names, client details, or operational metadata.

Mitigation: Treat query logs as sensitive data, limit exports to approved time windows and destinations, and review access controls before sharing or storing exported logs.

Risk: The skill depends on hologres-cli for SQL execution and GUC operations.

Mitigation: Pin and isolate hologres-cli before use, and review generated shell commands and SQL before execution.

## Reference(s):

- [Hologres Diagnostic SQL Queries](references/diagnostic-queries.md)
- [Hologres Slow Query Log Export](references/log-export.md)
- [Hologres Slow Query Log Configuration](references/configuration.md)
- [ClawHub Skill Page](https://clawhub.ai/wenbingyu/skills/hologres-slow-query-analysis)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with SQL and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include read queries, export steps, and database configuration commands that require review before execution.]

## Skill Version(s):

0.2.0 (source: server release evidence and VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
