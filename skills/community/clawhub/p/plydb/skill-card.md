## Description:

Skill for using the PlyDB CLI to perform SQL analysis across heterogeneous data sources including Postgres, MySQL, CSV, Parquet, JSON, Excel, SQLite, DuckDB, and Google Sheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ypt](https://clawhub.ai/user/ypt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data analysts use this skill to configure PlyDB data sources, run SQL across databases and files, fetch semantic context, and maintain OSI overlay files that enrich discovered data semantics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PlyDB can access configured databases, files, S3 objects, and Google Sheets using supplied credentials.

Mitigation: Review configuration files before use and prefer least-privilege database, cloud, and sheet credentials.

Risk: Google Sheets interactive OAuth may cache authorization for later PlyDB calls.

Mitigation: Have the user complete OAuth intentionally before agent-driven calls and confirm the cached account is appropriate for the requested data.

Risk: Generated SQL, config changes, or semantic overlays can produce incorrect analysis if they do not match the user's data model.

Mitigation: Review proposed queries and overlay edits with the user, especially before persisting new semantic context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ypt/skills/plydb)
- [PlyDB installation documentation](https://github.com/kineticloom/plydb?tab=readme-ov-file#installation)
- [Open Semantic Interchange (OSI)](https://github.com/open-semantic-interchange/OSI)
- [Database connections schema](references/config_schema.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON or YAML configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose SQL queries, PlyDB commands, config edits, and OSI semantic overlay updates; the artifact instructs agents to ask the user before creating or editing overlays.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
