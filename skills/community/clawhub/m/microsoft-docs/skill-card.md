## Description:

Query official Microsoft documentation to understand concepts, find tutorials, and learn how Azure, .NET, Microsoft 365, Windows, Power Platform, and other Microsoft technologies work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pdebruin](https://clawhub.ai/user/pdebruin)

### License/Terms of Use:


## Use Case:

Developers, engineers, and technical users use this skill to search and fetch official Microsoft Learn documentation for Microsoft services, tutorials, configuration options, limits, and best practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documentation queries may be sent to the configured Microsoft documentation service.

Mitigation: Avoid including secrets, proprietary details, or unnecessary personal data in documentation search and fetch queries.

Risk: Search excerpts may omit context needed for implementation decisions.

Mitigation: Fetch the full referenced page before relying on step-by-step configuration or limits guidance.

## Reference(s):

- [Microsoft Learn MCP Server](https://learn.microsoft.com/api/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text documentation search and fetch results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured Microsoft Learn MCP Server.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
