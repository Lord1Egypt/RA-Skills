## Description:

Converts natural-language database requests into SQL, can execute them against local or remote MySQL databases, and returns results in table, CSV, or JSON formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyesky](https://clawhub.ai/user/cyesky)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data practitioners use this skill to translate natural-language requests into MySQL queries, inspect schema, execute read and write statements, and return database results in a readable or exportable format.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute SQL against MySQL databases, including write, delete, drop, truncate, and transaction operations.

Mitigation: Use least-privilege database accounts and require review before any write, delete, drop, truncate, or transaction operation.

Risk: Database passwords may be exposed through command lines, logs, transaction output, or user-facing replies.

Mitigation: Avoid production credentials, avoid passing passwords on the command line, and mask passwords in all user-facing output.

Risk: Generated SQL may not match user intent or may affect more rows than expected.

Mitigation: Inspect schemas first, review generated SQL before execution, and confirm broad or destructive operations with the user.

## Reference(s):

- [NL2SQL Reference Guide](references/guide.md)
- [ClawHub skill page](https://clawhub.ai/cyesky/skills/nl2sql)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with SQL and bash code blocks plus table, CSV, or JSON query results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run MySQL helper scripts; passwords must be masked in any user-facing output.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
