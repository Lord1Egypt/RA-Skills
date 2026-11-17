## Description:

[FINANCIAL EXECUTION] Buy and sell meme coins and crypto tokens on Solana, BSC, Base, or Ethereum: single swap, multi-wallet batch trading, limit orders, stop loss, take profit, trailing stop loss, and trailing take profit via the GMGN API, with explicit user confirmation required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gmgnai](https://clawhub.ai/user/gmgnai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to prepare and execute GMGN CLI token swaps, multi-wallet trades, order status checks, gas-price queries, and trading strategies across Solana, BSC, Base, and Ethereum. It is intended for workflows where a human confirms each fund-moving action before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit irreversible blockchain transactions that move real funds.

Mitigation: Require explicit human confirmation before each swap or strategy creation, present resolved trade parameters, and start with low-value test funds.

Risk: The skill depends on persistent raw trading credentials that can authorize fund-moving actions.

Mitigation: Use only a low-value wallet, avoid exposing or logging credentials, rotate credentials if setup was already run, and prefer an externally managed secret store or wallet flow when available.

Risk: Global unpinned CLI installation can change trading behavior over time.

Mitigation: Review the installed CLI before use and avoid global unpinned installs for workflows that can trade funds.

Risk: Token addresses, amounts, chain choices, and API-returned values can be wrong or hostile.

Mitigation: Validate chain-specific address formats, quote shell arguments, run the required token security check before swaps, and require additional confirmation for high-risk tokens.

## Reference(s):

- [GMGN Skill Swap on ClawHub](https://clawhub.ai/gmgnai/skills/gmgn-swap)
- [GMGN API key setup](https://gmgn.ai/ai)
- [Solscan transaction explorer](https://solscan.io/tx/<hash>)
- [BscScan transaction explorer](https://bscscan.com/tx/<hash>)
- [BaseScan transaction explorer](https://basescan.org/tx/<hash>)
- [Etherscan transaction explorer](https://etherscan.io/tx/<hash>)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, parameter summaries, confirmations, and transaction receipts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include pre-trade confirmations, risk notes, order polling guidance, converted token amounts, order IDs, and block explorer links.]

## Skill Version(s):

1.4.6 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
