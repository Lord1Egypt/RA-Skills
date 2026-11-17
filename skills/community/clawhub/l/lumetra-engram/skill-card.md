## Description:

Persistent, explainable memory for OpenClaw agents that stores facts and recalls them later through Lumetra's hosted Engram MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brutus-gr](https://clawhub.ai/user/brutus-gr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to give OpenClaw agents persistent memory for user preferences, project facts, decisions, and other stable context. It supports storing, querying, listing, and deleting hosted memories through mcporter and the Engram MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation facts and memory queries may be sent to Lumetra's hosted service and processed by configured model providers.

Mitigation: Deploy only for data that is appropriate for hosted processing, avoid regulated or secret data, and require confirmation before storing memories.

Risk: The setup uses ENGRAM_API_KEY in mcporter configuration, which can expose access if stored or logged insecurely.

Mitigation: Use a narrowly scoped, revocable API key and review where mcporter stores authorization headers before deployment.

Risk: The skill includes delete and clear-memory operations that can remove persisted context.

Mitigation: Require explicit confirmation before deleting a memory or clearing a bucket.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/brutus-gr/skills/lumetra-engram)
- [Lumetra Homepage](https://lumetra.io)
- [Skill Repository](https://github.com/lumetra-io/engram-openclaw-skill)
- [Lumetra Models Configuration](https://lumetra.io/models)
- [Engram MCP Endpoint](https://mcp.lumetra.io/mcp/sse)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and MCP tool call selectors]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires mcporter and ENGRAM_API_KEY; calls a hosted memory service when configured.]

## Skill Version(s):

0.1.1 (source: server release evidence and OpenClaw metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
