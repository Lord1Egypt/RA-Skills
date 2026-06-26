## Description: <br>
Add liquidity, remove liquidity, or collect fees on Uniswap V2/V3/V4 pools, including pool selection, range optimization, approvals, safety checks, and transaction execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to manage Uniswap liquidity positions by adding liquidity, removing liquidity, or collecting accumulated fees with pool selection, range configuration, safety checks, and confirmation prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can drive real wallet approvals and transactions for Uniswap liquidity operations. <br>
Mitigation: Review the referenced liquidity-manager, pool-researcher, and Uniswap MCP setup before installation, and sign only after checking chain, token addresses, pool, amount, spender, approval limit, expiry, gas, slippage, and transaction summary. <br>
Risk: Private key handling may be unsafe if a raw private key is stored in plaintext environment files. <br>
Mitigation: Prefer a wallet, hardware signer, or secure secret manager instead of plaintext private keys. <br>
Risk: Token approvals can leave unused or excessive spending permissions. <br>
Mitigation: Use limited approvals where possible and revoke unused approvals after the liquidity action completes. <br>
Risk: Liquidity positions can expose users to impermanent loss, gas costs, low-liquidity pools, and range-management tradeoffs. <br>
Mitigation: Confirm pool liquidity, expected gas, range strategy, position size, and impermanent-loss exposure before executing any transaction. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wpank/manage-liquidity) <br>
- [Publisher profile](https://clawhub.ai/user/wpank) <br>
- [Skill specification](artifact/SKILL.md) <br>
- [Skill README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text transaction summaries with confirmation prompts and setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include pool details, position IDs, token amounts, fee estimates, explorer links, error guidance, and safety warnings.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
