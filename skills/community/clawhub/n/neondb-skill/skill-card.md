## Description: <br>
Manage Neon serverless Postgres databases, including projects, branches, databases, connection strings, and SQL queries for agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawbot-ved](https://clawhub.ai/user/clawbot-ved) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to manage Neon serverless Postgres projects, branches, databases, connection strings, and SQL workflows from command-line guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Neon API keys and database connection strings can grant access to managed Postgres resources if exposed. <br>
Mitigation: Use limited-scope credentials where possible, avoid pasting keys or connection strings into logs or chats, and rotate any exposed secrets. <br>
Risk: Database-management commands can delete or reset projects, branches, or databases. <br>
Mitigation: Review project, branch, and database IDs before destructive commands, and prefer isolated development branches for experiments. <br>
Risk: The bundled setup script provisions a Neon project, creates standard tables, and prints a pooled connection string. <br>
Mitigation: Run the script only when database provisioning is intended, store resulting credentials in secure configuration, and avoid exposing terminal output. <br>


## Reference(s): <br>
- [Neon](https://neon.tech) <br>
- [Neon Console](https://console.neon.tech) <br>
- [Neon API Docs](https://api-docs.neon.tech) <br>
- [Neon CLI Reference](https://neon.tech/docs/reference/neon-cli) <br>
- [neonctl GitHub Repository](https://github.com/neondatabase/neonctl) <br>
- [ClawHub Skill Page](https://clawhub.ai/clawbot-ved/neondb-skill) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/clawbot-ved) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash and SQL examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Neon CLI commands, psql examples, environment-variable guidance, and a setup script for standard organization tables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
