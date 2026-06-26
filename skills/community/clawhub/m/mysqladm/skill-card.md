## Description: <br>
MySQL database management via mysql CLI or Python mysql-connector for query execution, schema management, backup and restore, performance analysis, and user permission management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jasydongo](https://clawhub.ai/user/jasydongo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database administrators use this skill to operate MySQL databases through CLI-oriented guidance and helper scripts for querying, schema inspection and changes, backup and restore, performance analysis, and user permissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credentials may be exposed through command-line password arguments and environment-variable examples. <br>
Mitigation: Use MySQL option files or mysql_config_editor for credentials and avoid passing passwords directly on command lines. <br>
Risk: Bundled helper scripts construct shell command strings and execute them with eval. <br>
Mitigation: Remove eval-based command construction, pass arguments as arrays, and review commands before running the scripts. <br>
Risk: Restore and database administration examples include destructive actions such as dropping databases, grants, and SET GLOBAL changes. <br>
Mitigation: Require explicit confirmation for destructive restore or drop operations and test grants or SET GLOBAL changes in a non-production environment first. <br>


## Reference(s): <br>
- [MySQL Documentation](https://dev.mysql.com/doc/) <br>
- [Schema Analysis Reference](artifact/references/schema-analysis.md) <br>
- [Performance Tuning Reference](artifact/references/performance-tuning.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jasydongo/mysqladm) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, SQL, Configuration] <br>
**Output Format:** [Markdown with inline bash and SQL code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include database commands that should be reviewed before execution, especially against production systems.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
