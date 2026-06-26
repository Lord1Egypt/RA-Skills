## Description: <br>
Guides agents in using the mysql CLI to connect to MySQL databases, run queries and data changes, inspect schemas, manage transactions, and format results as JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[429668385](https://clawhub.ai/user/429668385) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database operators use this skill to inspect MySQL databases, run SQL statements, generate reports, import or export data, and troubleshoot schema or performance issues from an agent-controlled CLI workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents through broad MySQL write, delete, export, import, DDL, and transaction operations that could change or expose production data. <br>
Mitigation: Use least-privileged credentials, prefer read-only accounts by default, avoid production write access unless strictly needed, and require explicit approval after showing the exact SQL before INSERT, UPDATE, DELETE, DDL, LOAD DATA, export, script execution, or COMMIT operations. <br>
Risk: Database credentials and remote connections may expose secrets or sensitive data if handled casually. <br>
Mitigation: Avoid putting passwords directly on the command line, protect configuration files, require SSL for production connections, and limit agent access to only the databases and tables needed for the task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/429668385/mysql-database-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with mysql CLI commands, SQL snippets, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may execute live database reads, writes, exports, imports, DDL, or transactions depending on credentials and user approval.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
