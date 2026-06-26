## Description: <br>
GMGN Skill Swap helps an agent use gmgn-cli to quote, execute, monitor, and manage token swaps and strategy orders on Solana, BSC, Base, and Ethereum with explicit user confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gmgnai](https://clawhub.ai/user/gmgnai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and crypto traders use this skill to have an agent prepare, confirm, submit, and monitor GMGN token swaps, multi-wallet trades, limit orders, stop-loss orders, take-profit orders, trailing strategy orders, and gas-price checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute irreversible crypto trades with real funds. <br>
Mitigation: Install it only for intentional GMGN trading, use a low-balance wallet, and require explicit confirmation for every swap, multi-swap, and strategy order. <br>
Risk: The skill asks the agent to collect and persist GMGN API and private-key credentials. <br>
Mitigation: Configure secrets outside chat when possible, keep ~/.config/gmgn/.env permissions restricted, and remove any temporary private-key file after setup. <br>
Risk: Incorrect token addresses, amounts, or chain-specific options can cause failed or unintended transactions. <br>
Mitigation: Validate chain and address formats, convert token amounts to smallest units, run the required pre-swap token security check unless the user explicitly skips it, and present resolved trade parameters before execution. <br>


## Reference(s): <br>
- [ClawHub GMGN Skill Swap release page](https://clawhub.ai/gmgnai/gmgn-swap) <br>
- [GMGN API key setup](https://gmgn.ai/ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with gmgn-cli command examples, pre-trade confirmations, post-trade receipts, status summaries, and credential setup steps.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user confirmation before trade execution and reports transaction status, order IDs, and explorer links when available.] <br>

## Skill Version(s): <br>
1.4.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
