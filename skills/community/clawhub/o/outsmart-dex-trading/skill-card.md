## Description: <br>
Trade tokens on Solana via the outsmart CLI: buy, sell, quote, find pools, add/remove liquidity, claim fees, snipe, create pools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[outsmartchad](https://clawhub.ai/user/outsmartchad) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to draft Solana DEX trading, liquidity, pool discovery, balance, and token information commands for the outsmart CLI. It is not intended for Ethereum/EVM trading, centralized exchange orders, cross-chain bridges, or historical price analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a raw Solana private key and produce commands for irreversible fund-moving transactions. <br>
Mitigation: Install the external outsmart CLI only if trusted, use a dedicated low-balance wallet, and protect or remove ~/.outsmart/config.env when finished. <br>
Risk: Buy, sell, snipe, liquidity, fee-claim, and pool-creation commands can move funds or change on-chain positions. <br>
Mitigation: Require explicit user confirmation before every transaction command and prefer dry-runs before execution. <br>
Risk: Unknown or low-quality tokens can have poor liquidity, misleading volume, or total loss risk. <br>
Mitigation: Check token information before trading, start with small test buys, and size positions conservatively. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/outsmartchad/outsmart-dex-trading) <br>
- [Outsmart CLI homepage](https://github.com/outsmartchad/outsmart-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the outsmart CLI plus Solana wallet and RPC configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
