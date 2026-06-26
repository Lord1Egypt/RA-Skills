## Description: <br>
pg-copilot helps agents work with PostgreSQL by generating SQL from natural language, explaining SQL and results, creating Mermaid ERDs, suggesting performance improvements, managing partitions, and configuring database synchronization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiabusit](https://clawhub.ai/user/jiabusit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database engineers use this skill to inspect PostgreSQL schemas, generate or explain SQL, produce ERD diagrams, analyze query performance, manage table partitioning, and configure PostgreSQL-to-PostgreSQL or PostgreSQL-to-MySQL synchronization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has powerful database and synchronization access that can affect production data. <br>
Mitigation: Use dedicated least-privileged database accounts, test against non-production data first, review generated SQL before execution, and take backups before enabling synchronization or partition operations. <br>
Risk: Passwords and API keys may be exposed when passed on the command line or stored with weak protection. <br>
Mitigation: Prefer environment variables or a real secret manager, avoid command-line secrets, and rotate any credentials that may have been exposed. <br>
Risk: Configured external LLM endpoints may receive SQL text, schema details, or other sensitive database context. <br>
Mitigation: Configure external LLM endpoints only when that data is allowed to leave the environment, and review provider, endpoint, and retention requirements before use. <br>
Risk: Updates and deletes can propagate through synchronization targets. <br>
Mitigation: Confirm source and target tables, conflict behavior, retry settings, and monitoring before enabling sync, and verify target data after initial runs. <br>


## Reference(s): <br>
- [PostgreSQL cheatsheet](references/postgres-cheatsheet.md) <br>
- [ClawHub skill page](https://clawhub.ai/jiabusit/pg-copilot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with SQL, Mermaid, and shell command code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated SQL, natural-language explanations, EXPLAIN analysis, Mermaid ERD diagrams, and database synchronization setup guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
