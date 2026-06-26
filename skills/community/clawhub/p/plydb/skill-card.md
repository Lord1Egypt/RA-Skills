## Description: <br>
Skill for using the PlyDB CLI to perform SQL analysis across configured heterogeneous databases and files such as Postgres, MySQL, CSV, Parquet, JSON, Excel, SQLite, DuckDB, and Google Sheets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ypt](https://clawhub.ai/user/ypt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data analysts use this skill to configure PlyDB data sources, run SQL across databases and files, and gather semantic context for more accurate analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help an agent query configured databases, local files, cloud storage, and Google Sheets, which may expose sensitive data if access is broad. <br>
Mitigation: Use narrow configuration files, read-only database accounts, least-privilege cloud credentials, and only include local paths or S3 patterns that are needed for the task. <br>
Risk: Cached Google OAuth authorization can allow later agent-driven access to private sheets through the delegated account. <br>
Mitigation: Confirm which account is authorized, understand where tokens are stored, revoke tokens when no longer needed, and ask before querying private sheets. <br>


## Reference(s): <br>
- [Database connections schema](references/config_schema.md) <br>
- [Google Sheets OAuth troubleshooting](references/troubleshooting.md) <br>
- [PlyDB installation instructions](https://github.com/kineticloom/plydb?tab=readme-ov-file#installation) <br>
- [Open Semantic Interchange](https://github.com/open-semantic-interchange/OSI) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, SQL examples, JSON configuration, and YAML guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference configured data sources and semantic-context overlays supplied by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
