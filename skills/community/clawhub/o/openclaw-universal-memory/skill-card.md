## Description: <br>
Connector-agnostic Postgres + pgvector memory ingestion and retrieval with incremental cursor history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marcosathanasoulis](https://clawhub.ai/user/marcosathanasoulis) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure a Postgres-backed memory layer, ingest records from JSON or connectors, preserve cursor history, and search RAG-ready chunks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Database and connector operations are delegated to package code that was not included in the reviewed bundle. <br>
Mitigation: Install only after reviewing and trusting the actual openclaw_memory package and any connectors it will run. <br>
Risk: The skill can ingest private email, chat, task, or other account data into Postgres. <br>
Mitigation: Use it only for accounts and data you are authorized to process, and define retention and deletion rules before ingestion. <br>
Risk: Database credentials and DSNs may include sensitive passwords. <br>
Mitigation: Use environment or secret-store based DSN injection, avoid command-line passwords, and use least-privilege credentials limited to the intended memory tables. <br>


## Reference(s): <br>
- [OpenClaw Universal Memory on ClawHub](https://clawhub.ai/marcosathanasoulis/openclaw-universal-memory) <br>
- [Scheduling guide](docs/SCHEDULING.md) <br>
- [Connector setup walkthrough](docs/CONNECTOR_SETUP_WALKTHROUGH.md) <br>
- [Connector contribution guide](docs/CONNECTOR_CONTRIBUTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text, JSON] <br>
**Output Format:** [Markdown with inline bash commands and CLI text or JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python, local package installation, psycopg, a Postgres DSN, and pgvector-enabled Postgres.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
