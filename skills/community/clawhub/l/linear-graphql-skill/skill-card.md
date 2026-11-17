## Description:

Operate Linear workspace issues, projects, and teams through Linear GraphQL API using UXC.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:


## Use Case:

Developers and workspace operators use this skill to query Linear issues, teams, projects, and workflow states, and to create or update Linear records after confirming write intent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured credentials can grant access to Linear workspace data.

Mitigation: Use read-only or least-privilege credentials where possible and install the skill only for agents that should connect to the workspace.

Risk: Create, update, archive, and comment mutations can change Linear records.

Mitigation: Confirm the target workspace, issue IDs, and user intent before allowing write operations.

Risk: Literal API keys may be exposed if pasted directly into commands or logs.

Mitigation: Prefer environment-backed or managed secret storage for credentials and avoid literal API key entry unless necessary.

## Reference(s):

- [Linear API Documentation](https://developers.linear.app)
- [Linear GraphQL Schema](https://studio.apollographql.com/public/Linear-API)
- [Usage Patterns](references/usage-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Linear GraphQL query and mutation invocations that require configured credentials and user confirmation before writes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
