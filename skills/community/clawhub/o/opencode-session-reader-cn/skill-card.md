## Description:

Reads local OpenCode SQLite databases to list sessions, inspect message JSON, and check schema details across projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wufei-png](https://clawhub.ai/user/wufei-png)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to query local OpenCode session history, retrieve message JSON for a selected session, and inspect schema details without writing to the database.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose local OpenCode conversation history, prompts, code, command output, file paths, or secrets.

Mitigation: Use explicit invocation, approve the target project and session before reading message bodies, and avoid sharing retrieved message contents without review.

Risk: Implicit invocation can broaden access to local session data beyond the user's immediate intent.

Mitigation: Confirm the scope of each query before retrieving message bodies and prefer narrow project, session, and time filters.

Risk: OpenCode account-related tables may contain sensitive credentials or account data.

Mitigation: Avoid querying account or control_account tables.

## Reference(s):

- [OpenCode SQLite Schema Reference](references/schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and SQL command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only SQLite query guidance for local OpenCode databases.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
