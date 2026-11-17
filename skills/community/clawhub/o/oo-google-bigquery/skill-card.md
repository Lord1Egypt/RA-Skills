## Description:

Google BigQuery (cloud.google.com). Use this skill for ANY Google BigQuery request — reading, creating, updating, and deleting data. Whenever a task involves Google BigQuery, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inspect BigQuery projects, datasets, tables, jobs, and query results through an OOMOL-connected account, and to create or modify BigQuery resources when authorized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says potentially destructive SQL may be treated as safe to run directly.

Mitigation: Require user approval for SQL that changes data, including queries, and review the exact target and payload before execution.

Risk: The security review says setup runs an unverified remote installer and remote installer behavior is unverified.

Mitigation: Review and pin the CLI before installation, including bundled skill changes; restrict the connected BigQuery account to only required datasets and operations.

## Reference(s):

- [Google BigQuery](https://cloud.google.com/bigquery)
- [BigQuery REST API reference](https://cloud.google.com/bigquery/docs/reference/rest/v2)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [ClawHub skill release](https://clawhub.ai/oomol/skills/oo-google-bigquery)
- [Publisher profile](https://clawhub.ai/user/oomol)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, API calls]

**Output Format:** [Markdown instructions with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands can read data or request state changes in BigQuery; the skill instructs agents to seek confirmation for writes and destructive actions.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
