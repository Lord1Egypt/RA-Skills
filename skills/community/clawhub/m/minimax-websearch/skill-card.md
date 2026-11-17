## Description:

MiniMax Web Search lets agents run MiniMax Token Plan web search from OpenClaw, with fallback guidance for Brave Search and Qwen Chat when MiniMax is unavailable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godiao](https://clawhub.ai/user/godiao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to query web search through MiniMax in OpenClaw, especially on Windows setups where the upstream uvx launch path fails. It returns search results as JSON and documents fallback paths when a MiniMax subscription is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper runs mutable third-party MiniMax MCP code and launches Python through a shell while handling an API key.

Mitigation: Review before installing, use only a trusted pinned MiniMax MCP package version, and harden process launch behavior before sensitive use.

Risk: Search queries are sent to MiniMax or fallback providers.

Mitigation: Do not submit secrets or confidential data in search queries, and document approved provider use before deployment.

Risk: Untrusted configuration for MINIMAX_PYTHON or MINIMAX_API_HOST can redirect execution or traffic.

Mitigation: Set MINIMAX_PYTHON and MINIMAX_API_HOST only from trusted configuration and keep API keys in environment variables.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/godiao/skills/minimax-websearch)
- [Publisher profile](https://clawhub.ai/user/godiao)
- [Qwen Chat fallback](https://chat.qwen.ai)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON search result payloads and Markdown setup instructions with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a search query and MINIMAX_API_KEY; queries may be sent to MiniMax or fallback providers.]

## Skill Version(s):

1.0.1 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
