## Description:

Provides cryptocurrency trading analytics for Hyperbot, including smart money tracking, whale monitoring, market data queries, and trader statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[develophyperbotnetwork](https://clawhub.ai/user/develophyperbotnetwork)

### License/Terms of Use:


## Use Case:

Developers, AI agent users, and cryptocurrency analysts use this skill to query Hyperbot trading analytics and produce market, whale, smart-money, and trader-evaluation reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet addresses, query parameters, and session/query metadata are sent to the Hyperbot MCP service and related market-data providers.

Mitigation: Submit only wallet/query data you are comfortable sharing with those services, and avoid sensitive or personally identifying wallet sets unless you have consent and understand the provider's data handling.

Risk: Analytics and trading recommendations may influence financial decisions.

Mitigation: Treat outputs as informational and independently verify analysis before acting on trading or portfolio decisions.

Risk: The skill depends on external real-time market services and documented request limits.

Mitigation: Design agent workflows to handle unavailable, delayed, or rate-limited responses and retry only within the published limit of 100 requests per minute per IP.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/develophyperbotnetwork/skills/hyperbot-mcp)
- [Hyperbot MCP endpoint](https://mcp.hyperbot.network/mcp)
- [Prompts reference](references/prompts-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON-RPC examples and JSON-oriented analysis prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only MCP analytics; batch queries support up to 50 wallet addresses; rate limit is 100 requests per minute per IP.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact documentation lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
