## Description:

Call the IteraTools multi-tool API through MCP or REST for agent-accessible image, video, AI, memory, web, messaging, document, code, productivity, map, and utility tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fredpsantos33](https://clawhub.ai/user/fredpsantos33)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to connect agents to IteraTools' pay-per-use MCP server or REST API for broad tool access, including web automation, media processing, messaging, code execution, and productivity workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an unpinned local MCP package.

Mitigation: Prefer the remote MCP endpoint or a pinned, reviewed mcp-iteratools package version before local execution.

Risk: The integration exposes paid calls and x402 micropayments.

Mitigation: Require explicit approval for paid calls and use spending controls appropriate to the deployment.

Risk: The skill uses an IteraTools API key and could expose unrelated environment variables if run broadly.

Mitigation: Use a limited IteraTools API key and avoid exposing unrelated environment variables to the MCP process.

Risk: Available actions include messaging, code execution, browser automation, GitHub and Google changes, and sensitive-data handling.

Mitigation: Require explicit approval and tight scoping for these actions before an agent executes them.

## Reference(s):

- [IteraTools homepage](https://iteratools.com)
- [IteraTools documentation](https://docs.iteratools.com)
- [IteraTools tools reference](https://docs.iteratools.com/#tools-reference)
- [IteraTools API endpoint](https://api.iteratools.com)
- [IteraTools MCP endpoint](https://mcp.iteratools.com/mcp)
- [mcp-iteratools package](https://www.npmjs.com/package/mcp-iteratools)
- [IteraTools Smithery listing](https://smithery.ai/server/iterasoft/iteratools)
- [IteraTools GitHub project link](https://github.com/fredpsantos33/iteratools-mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown with shell, JSON, URL, and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may involve paid API or MCP tool calls and can include generated media, scraped content, messages, documents, code execution results, and productivity-system changes depending on the selected IteraTools tool.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
