## Description: <br>
Self-custodial Bitcoin Lightning wallet for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[satbot-mdk](https://clawhub.ai/user/satbot-mdk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill when an agent needs to initialize a self-custodial Lightning wallet, check balances, generate invoices, receive payments, or send bitcoin payments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store a wallet seed that controls real funds. <br>
Mitigation: Use small balances, back up and protect the mnemonic, and restrict permissions on ~/.mdk-wallet. <br>
Risk: The skill can send real bitcoin without clear approval safeguards. <br>
Mitigation: Require explicit confirmation before every outgoing payment. <br>
Risk: The skill runs a local wallet daemon and uses an npm package at execution time. <br>
Mitigation: Pin and verify the npm package version, and stop the daemon when it is not needed. <br>


## Reference(s): <br>
- [agent-wallet documentation](https://docs.moneydevkit.com/agent-wallet) <br>
- [@moneydevkit/agent-wallet npm package](https://www.npmjs.com/package/@moneydevkit/agent-wallet) <br>
- [ClawHub skill page](https://clawhub.ai/satbot-mdk/mdk-agent-wallet) <br>
- [Publisher profile](https://clawhub.ai/user/satbot-mdk) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands; wallet commands return JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and npx; installs and runs @moneydevkit/agent-wallet.] <br>

## Skill Version(s): <br>
0.3.3 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
