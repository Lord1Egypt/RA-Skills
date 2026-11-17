## Description:

Check and collect LP fees from PancakeSwap V3 and Infinity (v4) positions. Use when user says "collect my fees", "claim LP fees", "how much fees have I earned", "pending fees", "uncollected fees", "/collect-fees", "harvest LP fees", or asks about fees from a specific token pair position.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pcs-bot](https://clawhub.ai/user/pcs-bot)

### License/Terms of Use:

MIT-0

## Use Case:

External users and DeFi operators use this skill to discover pending PancakeSwap V3, Infinity, and Solana liquidity position fees, review fee summaries, and open PancakeSwap collection links. The skill is intended to read on-chain and API data and direct users to wallet-confirmed collection flows rather than execute transactions itself.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public wallet addresses and host or agent metadata may be sent to PancakeSwap, explorer, and RPC services.

Mitigation: Use the skill only when the user accepts those external queries; remove or disable the Step 0 ping where metadata reporting is not acceptable.

Risk: The skill installs npm packages at runtime without pinned versions.

Mitigation: Pin dependencies with a lockfile or approved package mirror before managed deployment.

Risk: Inherited endpoint overrides can redirect some Solana explorer requests.

Mitigation: Avoid inherited endpoint overrides and use trusted PancakeSwap or RPC providers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pcs-bot/skills/pcs-collect-fees)
- [PancakeSwap AI homepage](https://github.com/pancakeswap/pancakeswap-ai)
- [fetch-v3-positions.mjs](references/fetch-v3-positions.mjs)
- [fetch-infinity-positions.mjs](references/fetch-infinity-positions.mjs)
- [fetch-solana.cjs](references/fetch-solana.cjs)
- [viem readContract documentation](https://viem.sh/docs/contract/readContract)
- [PancakeSwap Infinity documentation](https://developer.pancakeswap.finance/contracts/infinity/overview)
- [PancakeSwap Liquidity UI](https://pancakeswap.finance/liquidity/pools)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown fee summaries with tables, JSON-derived values, shell command snippets, and PancakeSwap deep links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are read-oriented and direct users to PancakeSwap or wallet-confirmed flows for collection.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
