## Description: <br>
Full-stack dApp generation skill for Jovay blockchain, from requirements gathering to contract deployment and frontend debugging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jovay-developer](https://clawhub.ai/user/jovay-developer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to plan and generate Jovay Layer 2 EVM dApps, including Solidity contracts, tests, Vue 3 frontends, and testnet deployment steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet and deployment workflows can submit blockchain transactions or use funds on the wrong network. <br>
Mitigation: Use a dedicated low-value testnet wallet, confirm the network is testnet before signing, and review each transaction request. <br>
Risk: Generated smart contracts, deployment scripts, or frontend code may contain unsafe logic or defects. <br>
Mitigation: Review generated files, run tests, and perform appropriate security review before deploying or relying on the dApp. <br>
Risk: Private keys or wallet secrets can be exposed if placed in chat, shell commands, logs, or frontend code. <br>
Mitigation: Do not paste production secrets into agent conversations or generated code, and keep signing in wallet tooling such as MetaMask. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jovay-developer/jovay-dapp-skill) <br>
- [Jovay Sepolia testnet RPC](https://testnet-rpc.jovay.xyz) <br>
- [Jovay Sepolia testnet explorer](https://testnet-explorer.jovay.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with code snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Solidity contracts, Vue frontend files, Hardhat tests, and deployment commands for Jovay testnet workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
