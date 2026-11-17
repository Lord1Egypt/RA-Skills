## Description:

Hekkova is a permanent memory layer for AI agents that mints moments to the blockchain via MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hekkova](https://clawhub.ai/user/hekkova)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Hekkova to connect an AI agent to Hekkova's MCP endpoint, mint text, images, video, and public URLs as permanent moments, manage privacy phases, list or export archives, and check account balance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an unpinned MCP bridge with a Hekkova API key.

Mitigation: Use a pinned, audited bridge version and a narrowly scoped, revocable API key; do not log or store the key.

Risk: Selected content, URLs, and metadata are sent through the MCP bridge to Hekkova and can be minted permanently or publicly.

Mitigation: Avoid secrets, personal or regulated data, private or signed URLs, and content that may need deletion; use full_moon only for intentionally public content.

Risk: Minting and phase shifts consume paid credits, with higher cost for video.

Mitigation: Check balance before minting, confirm user intent for paid actions, and report credits remaining after successful mints.

## Reference(s):

- [Hekkova homepage](https://hekkova.com)
- [Hekkova dashboard](https://app.hekkova.com)
- [Hekkova MCP endpoint](https://mcp.hekkova.com/mcp)
- [ClawHub skill page](https://clawhub.ai/hekkova/skills/hekkova)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and MCP tool usage instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Block IDs, Token IDs, privacy phase, credits remaining, account details, and JSON or CSV exports through the MCP service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
