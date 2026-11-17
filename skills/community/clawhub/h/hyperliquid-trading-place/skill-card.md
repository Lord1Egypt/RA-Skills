## Description:

Places Hyperliquid perpetuals on explicit trade intent, requiring setup, builder-fee approval, user confirmation, and filled-order polling before treating a trade as complete.

This skill is ready for commercial/non-commercial use.

## Publisher:

[polyparlay](https://clawhub.ai/user/polyparlay)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading-agent operators use this skill to configure and run a Hyperliquid order-placement helper that only places trades after explicit intent and confirmation. It is intended for wallet-sensitive trading workflows where setup, fee approval, balance funding, and filled-order verification are part of the operating procedure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet-sensitive setup and trading code may access credentials during install or runtime.

Mitigation: Use isolated, low-balance or revocable trading credentials and avoid exposing a master private key through the shell environment.

Risk: The runtime depends on an unreviewed npm package for setup and trading behavior.

Mitigation: Verify the exact npm package contents and provenance before running npm install, setup, or the MCP helper.

Risk: Trading workflows can be mistaken for complete before an order is actually filled.

Mitigation: Require explicit trade confirmation and poll until fillStatus=FILLED before treating the trade as complete.

## Reference(s):

- [Hyperliquid Trading Place on ClawHub](https://clawhub.ai/polyparlay/skills/hyperliquid-trading-place)
- [polyparlay ClawHub publisher profile](https://clawhub.ai/user/polyparlay)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to run npm setup, start an MCP helper, request explicit trade confirmation, and poll until fillStatus=FILLED.]

## Skill Version(s):

1.0.32 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
