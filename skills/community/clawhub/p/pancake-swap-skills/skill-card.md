## Description:

BSC (Binance Smart Chain) trading on PancakeSwap -- wallet creation, token swaps, pair discovery, and balance management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kj-script](https://clawhub.ai/user/kj-script)

### License/Terms of Use:


## Use Case:

Developers and external users can use this skill to guide an agent through BSC wallet setup, BEP-20 token discovery, PancakeSwap quote checks, balance review, and user-confirmed swaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to persist and read BSC private-key material for signing swaps.

Mitigation: Use a dedicated low-balance wallet, prefer an encrypted keystore or external signer, restrict wallet file permissions, and review each swap before signing.

Risk: Optional ClawChain registration introduces an identity-binding path that may expose additional account linkage.

Mitigation: Skip ClawChain registration unless event tracking is explicitly needed, and review credential use before enabling that path.

Risk: Automated trading actions can lose funds through bad token addresses, poor liquidity, slippage, or transaction mistakes.

Mitigation: Require user confirmation, verify token contracts and liquidity, check quotes before execution, and keep funded amounts small.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kj-script/skills/pancake-swap-skills)
- [PancakeSwap](https://pancakeswap.finance)
- [PancakeSwap BSC Swap UI](https://pancakeswap.finance/swap?chain=bsc)
- [PancakeSwap V2 Contracts](https://docs.pancakeswap.finance/developers/smart-contracts/pancakeswap-exchange/v2-contracts)
- [BscScan](https://bscscan.com)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash, JavaScript, JSON, and transaction-flow examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes wallet file paths, environment variables, contract addresses, quote and swap flows, and security handling notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
