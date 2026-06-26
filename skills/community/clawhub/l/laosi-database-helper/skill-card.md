## Description: <br>
Database Helper Pro helps agents build SQL queries, manage database schemas, import and export CSV data, inspect SQLite databases, and draft ORM templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data analysts, and external users use this skill to generate database helper code, SQL examples, schema summaries, CSV import/export workflows, and ORM model templates. It is most directly evidenced for SQLite workflows, with the artifact describing optional MySQL and PostgreSQL dependencies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for broad SQL and database authority without clear safety boundaries for write or destructive operations. <br>
Mitigation: Use it with a restricted database account, preferably read-only unless writes are explicitly required. <br>
Risk: Generated CREATE, UPDATE, DELETE, DROP, import/export, or schema-change actions can modify or expose data. <br>
Mitigation: Require explicit confirmation before these actions and avoid production data unless backups and rollback procedures are in place. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/534422530/laosi-database-helper) <br>
- [Publisher profile](https://clawhub.ai/user/534422530) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python and SQL code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SQL statements, Python helper classes, CSV import/export examples, schema descriptions, and ORM templates.] <br>

## Skill Version(s): <br>
2.0.0 (source: release evidence, SKILL.md frontmatter, hub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
