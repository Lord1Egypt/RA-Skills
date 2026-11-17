## Description:

Money Toolkit helps agents provide finance-oriented guidance and run helper scripts for crypto arbitrage checks, DeFi yield comparisons, compound-interest estimates, and gas-fee comparisons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawto](https://clawhub.ai/user/clawto)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect public crypto market data, compare DeFi yield pools, estimate compound-return scenarios, and review gas-fee options. Outputs are informational and should not be treated as financial advice or transaction instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public market, DeFi, exchange, and blockchain RPC data can be delayed, unavailable, inaccurate, or incomplete.

Mitigation: Treat outputs as informational, verify market and protocol data independently, and avoid making financial decisions from a single script result.

Risk: The gas-fee helper depends on the web3 Python package and external RPC services.

Mitigation: Install web3 in a dedicated environment with pinned dependencies and review RPC endpoints before running the script.

Risk: The artifact provides finance-related guidance and calculations that could be misread as investment advice.

Mitigation: Present results with clear caveats, include fees and protocol risks in reviews, and require user confirmation before any real-world financial action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawto/skills/money-toolkit)
- [Publisher profile](https://clawhub.ai/user/clawto)
- [DeFiLlama Yields](https://defillama.com/yields)
- [DeFiLlama Yields API endpoint used by the artifact](https://yields.llama.fi/pools)
- [CoinGecko simple price API endpoint used by the artifact](https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd)
- [PublicNode Ethereum RPC endpoint used by the artifact](https://ethereum-rpc.publicnode.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with command examples and terminal-style text output from helper scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some helper scripts call public crypto, DeFi, exchange, and blockchain RPC services; the gas-fee script requires the web3 Python package.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
