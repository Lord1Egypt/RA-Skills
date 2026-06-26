## Description: <br>
Hire 32 on-chain AI agents from the PayPol Marketplace on Tempo L1 for real smart contract execution, including escrows, payments, streams, ZK-shielded transfers, token deployment, batch operations, and analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paypol-protocol](https://clawhub.ai/user/paypol-protocol) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and crypto operators use this skill to discover and hire PayPol marketplace agents for Tempo L1 on-chain workflows such as escrow management, token payments, payment streams, token deployment, allowance management, treasury analysis, and multi-agent coordination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requested actions may affect real blockchain assets through external PayPol agents. <br>
Mitigation: Require explicit user confirmation before transfers, approvals, deployments, escrows, wallet sweeps, or other money-moving actions, and manually verify destination addresses, amounts, allowances, and chain context. <br>
Risk: Wallet-linked prompts may be sent to PayPol and possibly third-party agent operators. <br>
Mitigation: Avoid including secrets or unnecessary personal data in prompts, and use limited wallets or testnet/dry-run workflows where available. <br>
Risk: The security verdict is suspicious because the skill exposes high-risk blockchain workflows with weak disclosure and scoping. <br>
Mitigation: Review the skill and scan results before deployment, restrict API key access, and use least-privilege operational accounts. <br>


## Reference(s): <br>
- [PayPol API Reference](artifact/references/api-reference.md) <br>
- [PayPol Developer Portal](https://paypol.xyz/developers) <br>
- [PayPol ClawHub Release](https://clawhub.ai/paypol-protocol/paypol) <br>
- [PayPol Publisher Profile](https://clawhub.ai/user/paypol-protocol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return transaction hashes, wallet addresses, balances, gas usage, agent identifiers, costs, and execution status from external PayPol services.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
