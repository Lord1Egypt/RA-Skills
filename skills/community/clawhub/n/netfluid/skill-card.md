## Description: <br>
Enables AI agents to process fiat and crypto payments, manage accounts, and handle multi-currency transfers via Netfluid. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jnysschensol](https://clawhub.ai/user/jnysschensol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use Netfluid to let agents query balances, onboard wallets, and initiate fiat or crypto payments, transfers, bridges, swaps, and withdrawals after account setup and KYC. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable real-money actions including signup, transfer, withdrawal, bridge, swap, and saved bank recipient operations. <br>
Mitigation: Require explicit human confirmation for each payment-sensitive action and verify recipient, amount, currency, fees, destination account or wallet address, and reversibility before execution. <br>
Risk: Wallet recovery phrases, API keys, session tokens, and PIN-backed sessions can grant broad wallet or payment authority. <br>
Mitigation: Use trusted MCP tooling only, keep credentials encrypted and out of logs or messages, and require human approval before any mnemonic-related action. <br>


## Reference(s): <br>
- [Netfluid on ClawHub](https://clawhub.ai/jnysschensol/netfluid) <br>
- [Netfluid website](https://netfluid.io) <br>
- [Netfluid compliance statement](https://go.netfluid.app/compliance) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Code, Configuration] <br>
**Output Format:** [Markdown with Python-style MCP tool call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Netfluid account credentials, wallet identifiers, API keys, session tokens, and explicit human confirmation for payment-sensitive actions.] <br>

## Skill Version(s): <br>
7.0.5 (source: server release evidence, README.md, and SKILL.md; package metadata lists 7.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
