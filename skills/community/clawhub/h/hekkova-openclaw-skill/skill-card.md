## Description:

Permanent memory layer for AI agents that mints moments to the blockchain via MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hekkova](https://clawhub.ai/user/hekkova)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect agents to Hekkova over MCP so they can mint, list, retrieve, phase-shift, and export permanent memories backed by Polygon, IPFS, and Filecoin.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Permanent or public storage can expose sensitive, regulated, private, or unauthorized third-party content if an agent mints the wrong material or changes a moment to full_moon.

Mitigation: Require explicit user confirmation before every mint, URL fetch, phase change to full_moon, and export; avoid secrets, private links, regulated data, and unauthorized third-party content.

Risk: The MCP connection uses an unpinned npx mcp-remote invocation that handles HEKKOVA_API_KEY.

Mitigation: Use a pinned or otherwise verified mcp-remote invocation, pass the API key only through the environment, and never echo, store, or log it.

Risk: Bulk exports can disclose the user's full Hekkova archive and metadata.

Mitigation: Confirm export scope and destination before running export_moments, and review the output before sharing it.

## Reference(s):

- [Hekkova homepage](https://hekkova.com)
- [Hekkova dashboard](https://app.hekkova.com)
- [Hekkova MCP endpoint](https://mcp.hekkova.com/mcp)
- [ClawHub skill page](https://clawhub.ai/hekkova/skills/hekkova-openclaw-skill)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API calls]

**Output Format:** [Markdown with inline shell commands and MCP tool guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference Hekkova Block IDs, Token IDs, privacy phases, credit balances, and JSON or CSV exports returned by MCP tools.]

## Skill Version(s):

1.2.1 (source: server release metadata and OpenClaw metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
