## Description:

Guides agents in using the mcp-local-rag MCP server for privacy-conscious web search, semantic ranking, and multi-engine research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nkapila6](https://clawhub.ai/user/nkapila6)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to choose and tune mcp-local-rag search tools for current web lookup, technical search, and multi-engine research while preserving privacy where possible.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP server installation can run mutable external code if the Git install or container image is not pinned.

Mitigation: Review the MCP server source and pin the Git install to a trusted commit or the Docker image to a verified digest before installing.

Risk: Search queries may expose secrets, personal data, or confidential research topics to selected search backends.

Mitigation: Avoid sending sensitive data through the search tools, especially when using Google or other non-private backends.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nkapila6/skills/local-rag-search)
- [mcp-local-rag MCP server](https://github.com/nkapila6/mcp-local-rag)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline tool calls and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results should include source URLs when available.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
