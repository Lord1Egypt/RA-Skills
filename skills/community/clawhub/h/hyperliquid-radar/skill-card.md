## Description:

Free Hyperliquid portfolio, funding, and wallet research for wallet reports, positions, fills, open orders, funding snapshots, and position health, intended for read-only analysis rather than trade placement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[polyparlay](https://clawhub.ai/user/polyparlay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to research public Hyperliquid wallets, positions, funding, margin, fills, open orders, and liquidation health. It is for read-only portfolio and wallet analysis, not for placing, canceling, or closing trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs pinned third-party MCP packages through npx.

Mitigation: Install only from trusted package publishers and distribution channels, keep the read-only Radar package pinned, and isolate any trading package from the research setup unless trading is explicitly intended.

Risk: Wallet research could expose sensitive user intent if private keys or seed phrases are provided.

Mitigation: Use only public 0x wallet addresses and never request, accept, or transmit private keys or seed phrases.

Risk: Trade placement is handled by a separate package and can create financial exposure.

Mitigation: Use the separate trading skill only after explicit trade, place, or execute intent, and keep normal Radar workflows read-only.

## Reference(s):

- [Hyperliquid Radar ClawHub Skill Page](https://clawhub.ai/polyparlay/skills/hyperliquid-radar)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown with inline shell commands and tool guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides use of a pinned read-only MCP package and the optional HYPELENS_NET environment variable for mainnet or testnet.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
