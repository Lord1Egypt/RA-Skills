## Description: <br>
Nara chain CLI agent for PoMI mining, wallet operations, transfers, quests, on-chain skills, ZK ID, and agent registry workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[naraguy](https://clawhub.ai/user/naraguy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate the naracli command-line workflow for Nara wallet setup, quest participation, agent registration, referrals, and NARA token actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide wallet, quest, staking, transfer, upload, skill-install, and agent-registration workflows that affect local secrets or on-chain state. <br>
Mitigation: Require fresh, explicit user approval for each transaction-like action and use a dedicated low-value wallet. <br>
Risk: Broad mining and reward triggers could lead the agent into wallet or on-chain workflows before the user has reviewed the package and source. <br>
Mitigation: Review the naracli npm package and source repository before installing or first running the CLI. <br>
Risk: Wallet secrets may be exposed if pasted into chat or displayed in logs. <br>
Mitigation: Never paste wallet secrets into chat, and do not display or log mnemonic phrases, private keys, or wallet file contents. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/naraguy/nara) <br>
- [Nara Homepage](https://nara.build) <br>
- [naracli npm Package](https://www.npmjs.com/package/naracli) <br>
- [naracli Source Repository](https://github.com/nara-chain/nara-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may operate on wallets or on-chain state and require explicit user approval for transaction-like actions.] <br>

## Skill Version(s): <br>
1.0.31 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
