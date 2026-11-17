## Description:

Search and debug production logs via Graylog with absolute or relative time queries, stream filtering, and system health checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pranavj17](https://clawhub.ai/user/pranavj17)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to search Graylog production logs, inspect recent or bounded time ranges, discover streams, and check Graylog health during debugging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Production log access and API-token use can expose sensitive operational data.

Mitigation: Use a dedicated read-only Graylog token with limited stream and search permissions, and store it only in environment configuration.

Risk: The skill relies on unverified npm execution for the Graylog MCP server.

Mitigation: Install only after verifying the npm package source or integrity, and pin the package version used by the configuration.

Risk: Broad triggers such as logs and debug logs can cause generic debugging prompts to access production logs.

Mitigation: Rename or scope triggers so production log searches require explicit Graylog intent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pranavj17/skills/graylog-log-search)
- [ClawHub publisher profile](https://clawhub.ai/user/pranavj17)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for read-only Graylog search and monitoring; actual log results depend on the configured Graylog instance and token permissions.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
