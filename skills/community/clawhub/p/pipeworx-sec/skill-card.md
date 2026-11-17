## Description:

Query the SEC EDGAR database to find companies, retrieve recent filings by form type, and access key financial metrics from XBRL data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to look up public companies, retrieve SEC filing metadata and document links, and inspect recent XBRL financial facts through a Pipeworx SEC MCP endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SEC lookup requests are routed through the disclosed Pipeworx gateway rather than directly to SEC systems.

Mitigation: Use the skill only when routing lookup arguments through that gateway is acceptable.

Risk: Tool arguments could accidentally include private notes, credentials, or unrelated sensitive data.

Mitigation: Send only the company identifiers, form types, and lookup parameters needed for SEC EDGAR queries.

## Reference(s):

- [Pipeworx sec ClawHub listing](https://clawhub.ai/brucegutman/skills/pipeworx-sec)
- [Pipeworx SEC MCP endpoint](https://gateway.pipeworx.io/sec/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with filing metadata, financial metrics, document links, curl examples, and MCP server configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses depend on SEC EDGAR availability and the disclosed Pipeworx gateway.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
