## Description:

Manage and query museum database records, track data collection status, verify completeness, and export museum data in JSON, CSV, or SQL formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackandking](https://clawhub.ai/user/jackandking)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data operators use this skill to inspect, validate, and export museum records stored in a MySQL database for cultural heritage data collection and reporting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad database access, including custom SQL execution and data exports.

Mitigation: Install only for databases you control, use a dedicated least-privilege account, and prefer read-only permissions for normal operation.

Risk: Database credentials and exported museum records can be exposed through process arguments, logs, or generated dump files.

Mitigation: Treat exports as sensitive, avoid logging credentials, store outputs in controlled locations, and rotate credentials if exposure is suspected.

Risk: User-supplied SQL can read or modify data beyond the intended workflow.

Mitigation: Do not let agents run arbitrary SQL without review, and avoid granting GRANT ALL or wildcard-host access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jackandking/skills/museum)
- [Artifact README](artifact/README.md)
- [Artifact skill documentation](artifact/SKILL.md)
- [Museum database schema](artifact/schema.sql)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI output; exports may be JSON, CSV, or SQL files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MySQL connection environment variables and invokes a local mycli executable.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
