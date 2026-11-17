## Description:

Guides agents in using Linkup search and fetch tools for query construction, search depth selection, output format choice, and web content retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shauryajain21](https://clawhub.ai/user/shauryajain21)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to guide web search, content extraction, company research, news retrieval, and data enrichment workflows through Linkup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill broadly encourages web and LinkedIn scraping, which can create privacy, compliance, or terms-of-service concerns.

Mitigation: Use it only for lawful, user-directed retrieval and avoid sensitive personal data collection unless there is a clear need and explicit direction.

Risk: Setup examples place an API key in URLs or shell commands where it may enter logs, shell history, or shared configuration.

Mitigation: Store credentials in a protected secret mechanism, avoid pasting real keys into commands or URLs, and rotate any key that may have been exposed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shauryajain21/skills/linkup-search)
- [Linkup MCPB Bundle](https://github.com/LinkupPlatform/linkup-mcp-server/releases/latest/download/linkup-mcp-server.mcpb)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with examples and inline command and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides query strategy, search depth selection, output type selection, and MCP setup guidance; does not execute searches itself.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
