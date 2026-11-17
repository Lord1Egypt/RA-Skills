## Description:

pg-copilot helps agents work with PostgreSQL by generating and explaining SQL, inspecting schemas, creating ERDs, analyzing performance, managing partitions, and configuring database synchronization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiabusit](https://clawhub.ai/user/jiabusit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database engineers use this skill to query, explain, document, tune, partition, and synchronize PostgreSQL databases through natural-language requests and CLI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Database and synchronization workflows can affect production data or important database state.

Mitigation: Review before installation, use least-privilege database accounts, and do not run sync-init or sync-watch on important databases until destructive behavior, SQL identifier quoting, confirmations, and secret storage are fixed.

Risk: Credentials and data may be exposed through command-line arguments, local configuration, LLM calls, or webhook destinations.

Mitigation: Avoid command-line secrets, rotate credentials previously stored with the skill, prefer environment-managed secrets, and restrict LLM and webhook destinations.

## Reference(s):

- [PostgreSQL cheatsheet](artifact/references/postgres-cheatsheet.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, SQL snippets, Mermaid ERD diagrams, JSON command output, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call configured database, LLM API, and webhook endpoints depending on the requested workflow.]

## Skill Version(s):

1.0.3 (source: server release evidence and user-provided target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
