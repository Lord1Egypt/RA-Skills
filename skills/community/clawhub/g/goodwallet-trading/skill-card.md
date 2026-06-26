## Description: <br>
Goodwallet Trading extends GoodWallet MPC agentic wallets with ERC20 transfers, token approvals, Uniswap V2 swaps, arbitrary contract calls, balance checks, and token information queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yoniassia](https://clawhub.ai/user/yoniassia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External GoodWallet users and developers use this skill to ask an agent to inspect token balances and prepare or execute Hoodi testnet ERC20 transfers, approvals, Uniswap V2 swaps, and contract calls through the GoodWallet flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad wallet-signing authority for transfers, approvals, swaps, and arbitrary contract calls. <br>
Mitigation: Require the agent to show the chain, recipient or contract, token, amount, spender, approval size, ETH value, calldata meaning, slippage, and expected effect before any transaction is allowed. <br>
Risk: Unlimited approvals and arbitrary contract calls can create consequences that are hard to reverse. <br>
Mitigation: Avoid unlimited approvals and arbitrary contract calls unless the user understands the exact consequence and has explicitly confirmed it. <br>
Risk: The skill depends on GoodWallet, the npm package, and the configured signing endpoint. <br>
Mitigation: Install and use it only when those components are trusted by the user or deployment owner. <br>


## Reference(s): <br>
- [Goodwallet Trading on ClawHub](https://clawhub.ai/yoniassia/goodwallet-trading) <br>
- [Hoodi Explorer](https://hoodi.etherscan.io/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and plain-language transaction results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should show user-facing transaction details before signing and avoid exposing internal credential paths, key formats, or signature details.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
