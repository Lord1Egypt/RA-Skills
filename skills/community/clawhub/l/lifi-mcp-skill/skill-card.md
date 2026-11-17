## Description:

Use the LI.FI MCP server through UXC for cross-chain route discovery, bridge/DEX availability checks, token and chain lookup, gas/balance/allowance checks, quote generation, and transfer status tracking without signing or broadcasting transactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to plan and monitor cross-chain swaps and bridges through LI.FI MCP, including chain and token discovery, route quoting, pre-execution checks, and status tracking without signing or broadcasting transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet addresses, API keys, quote requests, status checks, and balance checks can share financial metadata with LI.FI's hosted MCP endpoint.

Mitigation: Use wallet addresses and API keys only when needed, prefer environment variables for secrets, and avoid submitting unnecessary wallet or transaction details.

Risk: Quote and transaction request outputs could be mistaken for completed trades.

Mitigation: Present quotes and unsigned transactionRequest objects as planning outputs only; external wallet review, signing, and broadcast remain outside the skill.

Risk: Endpoint operation names or argument shapes can change over time.

Mitigation: Probe host and operation help before relying on an operation, then parse stable MCP envelope fields such as ok, kind, protocol, data, and error.

## Reference(s):

- [LI.FI MCP Usage Patterns](references/usage-patterns.md)
- [LI.FI MCP endpoint](https://mcp.li.quest/mcp)
- [ClawHub LI.FI MCP Skill](https://clawhub.ai/jolestar/skills/lifi-mcp-skill)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and JSON-output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides read-only MCP discovery, quote, balance, allowance, gas, and status workflows; it does not sign or broadcast transactions.]

## Skill Version(s):

1.0.0 (source: release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
