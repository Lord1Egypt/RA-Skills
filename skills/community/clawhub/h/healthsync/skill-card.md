## Description:

Queries Apple Health export data stored in a local SQLite database through the healthsync CLI or read-only SQLite queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bro3886](https://clawhub.ai/user/bro3886)

### License/Terms of Use:


## Use Case:

External users, developers, and analysts use this skill to inspect Apple Health export data in a local healthsync SQLite database, including heart rate, steps, sleep, workouts, energy, body metrics, mobility, and related trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recommended installer executes mutable remote code, and the alternate Go install command is unpinned.

Mitigation: Review the installer before use, prefer a pinned versioned release, and verify checksums or signatures where available.

Risk: Apple Health query results can expose sensitive health information in agent transcripts or logs.

Mitigation: Query only the minimum health fields needed and avoid retaining or sharing unnecessary result data.

Risk: Direct SQLite access could modify the local health database if write statements are issued.

Mitigation: Use read-only queries only and never run INSERT, UPDATE, DELETE, DROP, ALTER, or other write operations.

## Reference(s):

- [SQLite Schema Reference](artifact/references/schema.md)
- [healthsync installer](https://healthsync.sidv.dev/install)
- [ClawHub skill page](https://clawhub.ai/bro3886/skills/healthsync)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown with inline bash and SQL code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only query guidance for local Apple Health data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
