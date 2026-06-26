## Description: <br>
Helps agents generate MySQL queries and management commands for querying data, changing tables, backups, restores, and performance checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ding-renew](https://clawhub.ai/user/ding-renew) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and database operators use this skill to turn natural-language requests into MySQL SQL, client commands, and configuration guidance for queries, schema changes, backups, restores, and performance review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SQL may perform high-impact writes, deletes, schema changes, restores, or global setting changes. <br>
Mitigation: Use a read-only or least-privilege database account by default, review the exact SQL, and require explicit confirmation before UPDATE, DELETE, ALTER, DROP, RESTORE, SET GLOBAL, or large data operations. <br>
Risk: Database credentials or production privileges could be exposed or misused during MySQL operations. <br>
Mitigation: Avoid production write or admin credentials, keep secrets out of command history and prompts, and use scoped environment or client configuration for the minimum required access. <br>
Risk: Backup and restore commands can overwrite data or make recovery difficult if run against the wrong database. <br>
Mitigation: Verify the target database, test restore procedures outside production first, and keep a rollback path before running restore or bulk data commands. <br>


## Reference(s): <br>
- [MySQL Documentation](https://dev.mysql.com/doc/) <br>
- [MySQL Optimization Guide](https://dev.mysql.com/doc/refman/8.0/en/optimization.html) <br>
- [MySQL Workbench](https://www.mysql.com/products/workbench/) <br>
- [ClawHub Skill Page](https://clawhub.ai/ding-renew/mysql-skill-1-0-0-3) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with SQL, bash, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose high-impact SQL or shell commands that require review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
