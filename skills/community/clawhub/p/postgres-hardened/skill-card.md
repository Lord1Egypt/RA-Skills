## Description: <br>
PostgreSQL database patterns for query optimization, schema design, indexing, and security. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database engineers use this skill as a quick reference for PostgreSQL queries, migrations, schema design, indexing, RLS, connection pooling, and production safety checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Production PostgreSQL configuration changes can affect availability, performance, or access control if applied without review. <br>
Mitigation: Review current settings first, test changes in staging, confirm administrator privileges, and keep backups or rollback plans before applying impactful changes. <br>
Risk: SQL examples and database diagnostics can expose credentials or sensitive query text. <br>
Mitigation: Do not echo secrets back to users, use placeholders or bound parameters, and filter or hash pg_stat_statements query text before sharing it outside the database environment. <br>
Risk: Destructive DDL can cause irreversible data loss. <br>
Mitigation: Require a pg_dump backup, a rollback plan, and explicit confirmation for the specific destructive operation before generating or applying the change. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/snazar-faberlens/postgres-hardened) <br>
- [Faberlens safety evaluation](https://faberlens.ai/explore/postgres) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with SQL, shell, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include query examples, configuration templates, anti-pattern checks, and safety prompts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
