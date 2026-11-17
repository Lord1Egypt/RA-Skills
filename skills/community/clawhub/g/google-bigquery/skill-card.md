## Description:

Helps agents query and manage Google BigQuery data through a Maton-authenticated connection, with optional hosted functions and triggers for automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to run BigQuery SQL queries, inspect projects and data, and manage datasets, tables, and jobs through their authorized connection. Optional functions and triggers support scheduled or event-driven workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Maton connection may grant access to sensitive BigQuery data.

Mitigation: Authorize only the intended connection and narrowest OAuth scopes; avoid exposing credentials or full query responses.

Risk: Write, delete, and query jobs may change data or incur unintended work.

Mitigation: Default to read-only operations and review each write, delete, or query job with the user before approval.

Risk: Optional functions, triggers, and destinations may continue running or forwarding data.

Mitigation: Review automation and destinations before enabling them, and remove them when no longer needed.

## Reference(s):

- [ClawHub Google BigQuery skill](https://clawhub.ai/byungkyu/skills/google-bigquery)
- [Maton](https://maton.ai)
- [Maton documentation](https://docs.maton.ai)
- [BigQuery API reference](https://cloud.google.com/bigquery/docs/reference/rest)
- [BigQuery SQL query syntax](https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with command and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may contain sensitive data; show only the fields needed for the user's task.]

## Skill Version(s):

1.2.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
