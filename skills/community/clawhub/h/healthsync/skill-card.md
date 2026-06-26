## Description: <br>
Queries Apple Health data stored in a local SQLite database, including heart rate, steps, blood oxygen, VO2 Max, sleep, workouts, resting heart rate, HRV, blood pressure, energy, body metrics, mobility, running metrics, mindful sessions, wrist temperature, and related records through the healthsync CLI or direct SQLite in read-only mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BRO3886](https://clawhub.ai/user/BRO3886) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, technical users, and local agents use this skill to inspect Apple Health export data from a populated local healthsync SQLite database, generate focused CLI or SQL queries, and return health metrics in table, JSON, CSV, or summarized text form. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive Apple Health export records through broad CLI or SQL queries. <br>
Mitigation: Keep queries narrow, limit date ranges and row counts, and avoid sharing raw JSON or CSV health records unless the user explicitly needs them. <br>
Risk: Installation can rely on piping a remote installer script into a shell. <br>
Mitigation: Prefer a verifiable or pinned install method and install only when the user trusts the external healthsync CLI. <br>
Risk: The optional healthsync HTTP server can receive uploads and expose query endpoints if started without understanding its binding and security posture. <br>
Mitigation: Do not start the server unless the user requests it and understands how it is bound and secured. <br>
Risk: Direct SQLite access could modify or delete local health data if write operations are used. <br>
Mitigation: Use read-only CLI queries or read-only SQL only; do not run INSERT, UPDATE, DELETE, DROP, ALTER, or other write operations. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/BRO3886/healthsync) <br>
- [SQLite Schema Reference](references/schema.md) <br>
- [healthsync Installer](https://healthsync.sidv.dev/install) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, SQL snippets, and optional JSON or CSV query output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only query guidance for a local SQLite database populated by healthsync parse.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
