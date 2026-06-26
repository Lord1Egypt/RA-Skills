## Description: <br>
Connects agents to the Microsoft Learn MCP Server to search Microsoft documentation, fetch documentation pages, and find official code samples through mcporter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ricardodpalmeida](https://clawhub.ai/user/Ricardodpalmeida) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to connect an agent or terminal workflow to Microsoft Learn so they can look up Microsoft documentation, retrieve specific Learn pages, and find official code samples while working on Microsoft technologies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries, fetched URLs, and lookup prompts are sent to Microsoft's remote MCP endpoint. <br>
Mitigation: Avoid including secrets, private code, customer data, or confidential project details in Microsoft Learn lookup prompts. <br>
Risk: The Microsoft Learn MCP tool interface is dynamic and schemas may change. <br>
Mitigation: List the current tools and schemas before use, and refresh the schema when calls fail or behavior changes. <br>


## Reference(s): <br>
- [Microsoft Learn MCP Reference](references/mcp-details.md) <br>
- [Microsoft Learn MCP endpoint](https://learn.microsoft.com/api/mcp) <br>
- [Microsoft Learn MCP best practices](https://learn.microsoft.com/en-us/training/support/mcp-best-practices) <br>
- [Microsoft Learn MCP FAQ](https://learn.microsoft.com/en-us/training/support/mcp-faq) <br>
- [Microsoft Learn MCP release notes](https://learn.microsoft.com/en-us/training/support/mcp-release-notes) <br>
- [Official MicrosoftDocs MCP repository](https://github.com/MicrosoftDocs/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include human-readable or JSON mcporter output depending on command flags.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
