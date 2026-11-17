## Description:

Agify MCP provides age prediction from a first name using agify.io without authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query Pipeworx's Agify MCP endpoint for first-name age-prediction data and receive JSON-RPC responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP client configuration uses mcp-remote@latest, which can execute changing third-party code locally.

Mitigation: Review before installing and prefer a pinned, reviewed MCP bridge version.

Risk: Name queries are sent to Pipeworx and may reach Agify, so sensitive or personal data could leave the local environment.

Mitigation: Use only non-sensitive first-name age-prediction queries and avoid submitting confidential or identifying context.

## Reference(s):

- [Pipeworx Agify Pack](https://pipeworx.io/packs/agify)
- [Pipeworx](https://pipeworx.io)
- [Pipeworx Agify MCP endpoint](https://gateway.pipeworx.io/agify/mcp)
- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-agify)
- [Publisher profile](https://clawhub.ai/user/brucegutman)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON-RPC examples and MCP client configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses from the service are JSON-RPC 2.0 payloads; anonymous use is rate limited.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
