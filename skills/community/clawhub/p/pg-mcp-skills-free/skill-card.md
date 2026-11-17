## Description: <br>
PG-MCP Assistant Free helps developers use PostgreSQL MCP tools for database health checks, index tuning, query-plan analysis, schema lookup, SQL execution, and related operational workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to manage PostgreSQL databases from an agent conversation, especially for development and test workflows such as health checks, schema inspection, slow-query diagnosis, and guarded SQL execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SQL or MCP-backed database actions can modify or delete PostgreSQL data when the configured server has write permissions. <br>
Mitigation: Use read-only MCP credentials for production, review every SQL statement, and approve UPDATE, DELETE, DROP, INSERT, or ALTER only when the database change is intended. <br>
Risk: Database operations can exceed the intended scope if the MCP server is configured with overly broad database permissions. <br>
Mitigation: Install the skill only where the PostgreSQL MCP server has permissions appropriate for the databases the agent should manage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/pg-mcp-skills-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with SQL examples, command suggestions, and JSON-style structured responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose MCP tool usage, PostgreSQL SQL statements, setup steps, and operational recommendations; write operations require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
