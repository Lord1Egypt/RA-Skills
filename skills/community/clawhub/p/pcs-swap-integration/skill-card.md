## Description: <br>
Integrates PancakeSwap swaps into frontends, backends, and smart contracts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pcs-bot](https://clawhub.ai/user/pcs-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers building PancakeSwap swap experiences use this skill for routing quotes, SDK and Universal Router integration, direct V2 router swaps, and transaction troubleshooting across supported EVM chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples include wallet signing and transaction broadcasting that can affect real funds. <br>
Mitigation: Use testnet or low-value wallets first, and verify chain, token, amount, recipient, slippage, and deadline before broadcasting any transaction. <br>
Risk: Approval examples include broad token allowances. <br>
Mitigation: Review every spender address and allowance, prefer bounded approvals, and avoid approving contracts that have not been independently verified. <br>
Risk: Prompts or generated scripts could expose private keys or run with unintended wallet authority. <br>
Mitigation: Do not paste private keys into prompts, keep secrets in the local runtime environment, and inspect generated scripts before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pcs-bot/pcs-swap-integration) <br>
- [PancakeSwap AI repository](https://github.com/pancakeswap/pancakeswap-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with TypeScript, Solidity, JSON, and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes blockchain addresses, package installation commands, API examples, approval guidance, and transaction troubleshooting notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
