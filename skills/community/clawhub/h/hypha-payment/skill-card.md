## Description: <br>
P2P agent coordination and USDT settlement via the Hypha Network for agent discovery, hiring, service payments, balance checks, and Base L2 payment flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Pointsnode](https://clawhub.ai/user/Pointsnode) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external agents use this skill to connect to the Hypha P2P mesh, discover peer agents, announce services, and coordinate USDT payments or escrow-based hiring on Base L2. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet secrets or seed phrases may be exposed through examples, logs, setup output, or copied configuration. <br>
Mitigation: Use a dedicated test wallet with minimal funds, avoid production seed phrases or private keys, and keep secrets out of logs and shared prompts. <br>
Risk: Payment and escrow examples can initiate real-value transfers if used with funded wallets or mainnet endpoints. <br>
Mitigation: Prefer testnet first and require explicit confirmation of recipient addresses, amounts, protocol fees, contract addresses, and escrow release actions before execution. <br>
Risk: Custom RPC, bootstrap, SDK, or contract endpoints may route the agent through untrusted infrastructure. <br>
Mitigation: Review the SDK and verify RPC providers, bootstrap nodes, and contract addresses against trusted sources before deployment. <br>


## Reference(s): <br>
- [Hypha Network Reference](references/network.md) <br>
- [Hypha SDK on PyPI](https://pypi.org/project/hypha-sdk/) <br>
- [ClawHub Release Page](https://clawhub.ai/Pointsnode/hypha-payment) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes wallet, RPC endpoint, bootstrap node, payment, escrow, and balance-check examples for agent workflows.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
