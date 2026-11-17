## Description:

PostgreSQL database management tool for querying databases, exporting results, inspecting schemas, and performing UPDATE/DELETE operations with backup and recovery workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuzongwen](https://clawhub.ai/user/liuzongwen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, database operators, and support engineers use this skill to inspect PostgreSQL schemas, run bounded SELECT queries, export query results, and prepare database maintenance commands. It also provides guidance for backup, confirmation, and recovery steps around UPDATE and DELETE workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Database-change safeguards, including backup, restore, force, and dry-run protections, may not be reliable enough for production data without review.

Mitigation: Review and test the code in a controlled environment before installation, use SELECT previews, keep independent backups, and avoid production UPDATE or DELETE workflows until fixes are validated.

Risk: Bundled database configuration includes default postgres/postgres credentials.

Mitigation: Remove the bundled config before use and provide environment-specific credentials for a dedicated least-privilege PostgreSQL role.

Risk: Generated backups may contain sensitive database rows and are written by the skill workflow.

Mitigation: Store backups outside the skill package with restricted permissions, retention controls, and appropriate handling for sensitive data.

Risk: Dependency installation guidance can introduce unverified packages or elevated-permission installation practices.

Mitigation: Pin and verify dependencies, prefer user or virtual environment installs, and avoid sudo or administrator installation unless separately approved.

## Reference(s):

- [Quick Reference](references/QUICK_REFERENCE.md)
- [Safety Guide](references/SAFETY_GUIDE.md)
- [Examples](references/EXAMPLES.md)
- [Offline Deployment Guide](references/OFFLINE_DEPLOYMENT_GUIDE.md)
- [Scripts README](scripts/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code]

**Output Format:** [Markdown guidance with inline shell commands and generated CSV, Excel, JSON, or terminal table output depending on the workflow.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create query exports and database backup metadata files when the script workflows are used.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
