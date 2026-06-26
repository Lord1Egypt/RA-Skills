## Description: <br>
Helps agents produce jovay-cli guidance and commands for wallet, token, contract, network, and bridge interactions on Jovay and Ethereum. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryogawan](https://clawhub.ai/user/ryogawan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and blockchain operators use this skill to ask an agent for Jovay CLI commands for wallet setup, balance checks, transfers, approvals, contract calls, network switching, and ETH bridge operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet setup and transaction workflows can expose private keys or encryption passwords if users paste secrets directly into shell commands. <br>
Mitigation: Use a dedicated low-balance wallet, avoid passing private keys or wallet passwords on the command line when possible, and enable encrypted wallet storage. <br>
Risk: Commands using --broadcast can send irreversible blockchain transactions with the wrong network, recipient, contract, token, amount, gas, or spender. <br>
Mitigation: Manually confirm every transaction parameter, verify the jovay-cli package provenance, and review each --broadcast command before execution. <br>


## Reference(s): <br>
- [Jovay Network Information](https://docs.jovay.io/developer/network-information) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may include wallet, contract, bridge, network, and transaction parameters that require user review before execution.] <br>

## Skill Version(s): <br>
0.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
