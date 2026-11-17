## Description:

HyperNatt Terminal helps agents connect to a remote MCP that exposes six crypto market-data and swap-routing tools, with no local shell, filesystem, or environment-variable access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dialloube-research](https://clawhub.ai/user/dialloube-research)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading-agent builders use this skill to onboard an agent to the HyperNatt remote MCP for liquidation radar, execution-context checks, and user-signed swap routing. It provides call order and safety guidance; it is not trade advice and does not submit orders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting an agent to a remote crypto MCP can expose users to paid x402 USDC calls or user-signed swap routes.

Mitigation: Confirm the user is comfortable with remote MCP use and payment authorization rules before paid calls or swap routing; use only host-approved wallet authorization.

Risk: Wallet handling mistakes could expose sensitive credentials.

Mitigation: Do not request private keys or scrape environment secrets; rely on the buyer wallet already configured in the host application.

Risk: Market-data and execution-context outputs may be mistaken for trade advice or order execution.

Mitigation: Present outputs as informational context only, make clear that the skill is not trade advice, and require the user or host application to sign or submit any transaction separately.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dialloube-research/skills/hypernatt-terminal)
- [HyperNatt Platform](https://hypernatt.com)
- [HyperNatt MCP Protocol](https://hypernatt.com/mcp/protocol)
- [HyperNatt MCP Server Card](https://hypernatt.com/.well-known/mcp/server-card.json)
- [Coinbase Agentic Wallet MCP Documentation](https://docs.cdp.coinbase.com/agentic-wallet/mcp/welcome)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration]

**Output Format:** [Markdown with JSON MCP call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote MCP onboarding only; no local execution, filesystem access, or environment variables.]

## Skill Version(s):

1.6.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
