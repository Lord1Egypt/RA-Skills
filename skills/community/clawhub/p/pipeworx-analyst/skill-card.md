## Description:

Pipeworx Analyst connects an agent to Pipeworx's remote data gateway so users can ask natural-language questions across trade, finance, pharma, housing, government contracting, weather, filings, and related data sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to connect an agent to Pipeworx's MCP gateway and query multiple public and business data domains in natural language, with optional task-scoped sessions for narrower tool access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends broad user questions and persistent context to an external Pipeworx gateway without enough privacy, scoping, or retention detail in the available evidence.

Mitigation: Use task-scoped gateway URLs where possible, avoid sending secrets, regulated personal data, credentials, or confidential business information, and confirm Pipeworx retention, deletion, isolation, and access controls before sensitive use.

Risk: The remember and recall behavior can preserve findings across tool calls, which may retain sensitive context if used carelessly.

Mitigation: Do not use remember or recall for sensitive findings unless Pipeworx separately documents controls that satisfy the deployment requirements.

Risk: The gateway can select from a large set of tools and data domains, which may produce overly broad or unexpected external queries.

Mitigation: Prefer task-scoped sessions and review response metadata, tool choice, and error alternatives before relying on returned results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-analyst)
- [Publisher profile](https://clawhub.ai/user/brucegutman)
- [Pipeworx MCP gateway](https://gateway.pipeworx.io/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or plain text responses with JSON configuration snippets for setup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include metadata with cost breakdown, cache status, next-step suggestions, and error alternatives.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
