## Description:

Instant DB helps agents work with InstantDB apps by querying data, creating, updating, deleting, linking, and unlinking entities, running transactions, and subscribing to real-time changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ubyjerome](https://clawhub.ai/user/ubyjerome)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to administer InstantDB-backed workflows, including live database queries, entity mutations, relationship updates, transactions, and real-time progress monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent live admin-level read, write, delete, link, unlink, and transaction access to an InstantDB app.

Mitigation: Install only for intended apps, use a dedicated admin token where possible, and prefer staging environments or backups before write and delete operations.

Risk: Secrets such as the InstantDB admin token could be exposed through prompts, logs, or client code.

Mitigation: Keep admin tokens in environment variables or a secrets manager and avoid echoing them into prompts, logs, generated code, or browser-side applications.

Risk: Delete, unlink, cascade delete, and bulk transaction operations can cause irreversible data loss or broad relationship changes.

Mitigation: Require explicit user confirmation for destructive or bulk operations and review the target namespace, entity IDs, and transaction payload before execution.

## Reference(s):

- [InstantDB documentation](https://www.instantdb.com/docs)
- [InstantDB Admin SDK](https://www.instantdb.com/docs/admin)
- [InstantDB Query Syntax Reference](references/query_syntax.md)
- [InstantDB Transaction Patterns](references/transactions.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute InstantDB admin API operations when configured with an app ID and admin token.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
