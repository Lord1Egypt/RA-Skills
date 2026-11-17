## Description:

Full-stack dApp generation skill for Jovay blockchain — from requirements gathering to contract deployment and frontend debugging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jovay-developer](https://clawhub.ai/user/jovay-developer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan, scaffold, implement, test, and deploy full-stack Jovay Layer 2 EVM dApps with Solidity contracts and a Vue 3 frontend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet or private-key exposure during dApp deployment.

Mitigation: Use a disposable testnet wallet, avoid real private keys in shell commands or frontend code, and confirm the selected network before deployment.

Risk: Unpinned npm packages or template scripts may execute code the user has not reviewed.

Mitigation: Inspect generated project scripts and dependencies before running them, prefer pinned versions, and use an isolated container when possible.

Risk: Generated smart contracts can contain functional or security defects.

Mitigation: Compile, test, review access control and fund-handling logic, and verify deployed contract addresses on the Jovay testnet explorer before broader use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jovay-developer/skills/jovay-dapp-skill)
- [Jovay Sepolia testnet RPC](https://testnet-rpc.jovay.xyz)
- [Jovay Sepolia testnet explorer](https://testnet-explorer.jovay.xyz)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code blocks, shell commands, Solidity, JavaScript, and Vue snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose project files, smart contracts, frontend code, deployment steps, and local debugging commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
