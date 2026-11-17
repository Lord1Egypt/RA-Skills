## Description:

Places Hyperliquid perpetual futures orders only after explicit trade intent, post-install setup, builder-fee approval, account funding, and confirmTrade authorization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[polyparlay](https://clawhub.ai/user/polyparlay)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading-agent operators use this skill to configure Hyperliquid MCP tooling and place mainnet perpetual futures orders after explicit trade, place, or execute intent. It is intended for users who understand wallet authority, builder fees, funding requirements, and post-fill stop management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs third-party npm code and may modify local MCP configuration.

Mitigation: Review setup behavior and dependency versions before installation, pin the dependency tree with a lockfile where possible, and run setup only in an environment intended for this skill.

Risk: The skill handles real-wallet authority and can approve builder-fee authority before trades are placed.

Mitigation: Use a dedicated low-balance wallet and avoid exposing a master private key to the npm install environment unless the approval flow and fee settings have been reviewed.

Risk: Mainnet trading can place real Hyperliquid perpetual futures orders after explicit confirmation.

Mitigation: Require explicit trade, place, or execute intent with confirmTrade set to true, verify account funding and maxBuilderFee status, and review order parameters before use.

Risk: Filled positions create ongoing market risk after execution.

Mitigation: Install and configure a stop-management companion such as agent-guard, pm-desk, or polymarket-stops, and call the heartbeat flow before increasing size.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/polyparlay/skills/hyperliquid-place)
- [Hyperliquid app](https://app.hyperliquid.xyz)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown with inline shell commands and MCP tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and npm; post-install setup wires MCP configuration before trading tools can run.]

## Skill Version(s):

1.3.65 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
