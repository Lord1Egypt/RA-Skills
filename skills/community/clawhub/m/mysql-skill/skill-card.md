## Description: <br>
Helps agents generate SQL and shell commands for MySQL querying, data analysis, schema management, backup, restore, and performance checks from natural-language requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryanlee-gemini](https://clawhub.ai/user/ryanlee-gemini) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, database administrators, and data analysts use this skill to translate natural-language database tasks into MySQL queries, administration commands, backup and restore workflows, and optimization guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce high-impact MySQL write, delete, schema-change, backup-overwrite, or restore actions. <br>
Mitigation: Use a dedicated least-privilege account, prefer read-only credentials for analysis, and require explicit manual review and confirmation before execution. <br>
Risk: Database credentials and credential files may be exposed if handled carelessly. <br>
Mitigation: Protect credential files and environment variables, and avoid placing plaintext passwords in command-line arguments or shared logs. <br>
Risk: The security evidence flags unclear confirmation safeguards for production database operations. <br>
Mitigation: Treat production changes as approval-gated proposals and verify backups before write, delete, schema-change, overwrite, or restore operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryanlee-gemini/mysql-skill) <br>
- [MySQL documentation](https://dev.mysql.com/doc/) <br>
- [MySQL optimization documentation](https://dev.mysql.com/doc/refman/8.0/en/optimization.html) <br>
- [MySQL Workbench](https://www.mysql.com/products/workbench/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with SQL, shell, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include database administration actions that require human review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
