## Description:

Cryptocurrency prices, market cap rankings, and fiat currency conversion via CoinGecko

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve live cryptocurrency prices, ranked market data, and fiat exchange-rate conversions for portfolio, pricing, and market-overview workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP configuration runs mcp-remote from the mutable latest tag at startup.

Mitigation: Prefer a pinned mcp-remote version and review dependency behavior before using the skill in sensitive environments.

Risk: Crypto and currency lookup requests are sent to the Pipeworx gateway.

Mitigation: Use the skill only when sharing those lookup requests with the remote service is acceptable, and avoid exposing nearby sensitive files or credentials.

## Reference(s):

- [Pipeworx crypto homepage](https://pipeworx.io/packs/crypto)
- [Pipeworx crypto MCP endpoint](https://gateway.pipeworx.io/crypto/mcp)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [Tool responses with Markdown guidance, JSON examples, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for direct examples and uses a remote MCP endpoint for live market and exchange-rate lookups.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
