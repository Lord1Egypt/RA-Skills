## Description: <br>
Store and query structured data without planning schemas upfront. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marcosnataqs](https://clawhub.ai/user/marcosnataqs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use KameleonDB to give agents persistent structured storage for contacts, tasks, knowledge bases, imported data, user preferences, and other state that can evolve over time without upfront schema planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents using this skill can persist, query, import, change schemas, and delete records in a database. <br>
Mitigation: Use an isolated agent-only or test database, least-privilege credentials, backups, and explicit approval rules for destructive or schema-changing operations. <br>
Risk: Persistent storage can capture personal data or sensitive user preferences across conversations. <br>
Mitigation: Define clear rules for what may be stored, require user consent where appropriate, and avoid storing sensitive data unless the deployment has matching privacy controls. <br>
Risk: Direct SQL and broad import workflows can create misleading records or unintended data exposure. <br>
Mitigation: Review generated SQL and imported files before execution, avoid production credentials, and scope database access to the minimum tables and operations required. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/marcosnataqs/kameleondb) <br>
- [KameleonDB Homepage](https://github.com/marcosnataqs/kameleondb) <br>
- [PyPI Package](https://pypi.org/project/kameleondb/) <br>
- [First Principles](https://github.com/marcosnataqs/kameleondb/blob/main/FIRST-PRINCIPLES.md) <br>
- [Architecture Guide](https://github.com/marcosnataqs/kameleondb/blob/main/docs/ARCHITECTURE.md) <br>
- [Example Agent-Driven Data Modeling Workflow](examples/workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, SQL queries, JSON] <br>
**Output Format:** [Markdown with inline bash, SQL, JSON, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the kameleondb command-line tool and KAMELEONDB_URL environment variable.] <br>

## Skill Version(s): <br>
0.1.5 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
