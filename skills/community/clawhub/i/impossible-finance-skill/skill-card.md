## Description: <br>
BSC (Binance Smart Chain) trading on Impossible Finance DEX: wallet creation, token swaps, pair discovery, and balance management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KJ-Script](https://clawhub.ai/user/KJ-Script) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to configure an agent-assisted BSC wallet, discover Impossible Finance swap paths, check balances, and prepare token swap transactions with user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent-assisted BSC trading wallet can lose funds if private keys are exposed or if the wallet holds more value than intended. <br>
Mitigation: Use a fresh low-balance wallet, keep wallet.json encrypted or chmod 600, and never use a main wallet or funds you cannot afford to lose. <br>
Risk: Incorrect token addresses, amounts, slippage settings, approvals, or transactions can cause unwanted trades or loss. <br>
Mitigation: Verify every token address, amount, slippage setting, approval, and transaction before signing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/KJ-Script/impossible-finance-skill) <br>
- [Impossible Finance](https://impossible.finance) <br>
- [Impossible Finance Swap](https://app.impossible.finance/swap) <br>
- [Impossible Finance Docs](https://docs.impossible.finance) <br>
- [BSC explorer](https://bscscan.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JavaScript examples, JSON snippets, and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include wallet setup steps, BSC transaction preparation guidance, swap path checks, and transaction hashes for user review.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact frontmatter says 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
