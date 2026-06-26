## Description: <br>
Health Data Analyzer helps agents query and analyze sleep, exercise, recovery, heart-rate variability, blood oxygen, and related health data through a connected healthdata MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianchuanjun64-afk](https://clawhub.ai/user/tianchuanjun64-afk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect health database tables, query scoped date ranges, and produce health summaries, trend analysis, and personalized recommendations from connected sleep, training, and recovery data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive health, account, and device metadata from the connected healthdata MCP server. <br>
Mitigation: Install only when this access is intended, use explicit prompts, and treat terminal output and logs as sensitive health information. <br>
Risk: Broad table queries or long date ranges can expose more health data than needed for a question. <br>
Mitigation: Use narrow date ranges and query only the tables needed for the requested analysis; avoid users and user_data_sources unless identity or device provenance is specifically required. <br>


## Reference(s): <br>
- [Health Data Analyzer ClawHub page](https://clawhub.ai/tianchuanjun64-afk/health-data-analyzer) <br>
- [Publisher profile](https://clawhub.ai/user/tianchuanjun64-afk) <br>
- [Query Patterns](references/query-patterns.md) <br>
- [Database Schema](references/database-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON query results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may contain sensitive health, account, and device metadata from the connected MCP server.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
