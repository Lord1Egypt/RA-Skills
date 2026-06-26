## Description: <br>
Full-stack dApp generation skill for Jovay blockchain, from requirements gathering to contract deployment and frontend debugging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryogawan](https://clawhub.ai/user/ryogawan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to gather dApp requirements, scaffold Jovay projects, generate Solidity contracts and Vue 3 frontends, and deploy or debug on the Jovay testnet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide wallet setup and blockchain transactions during testnet deployment. <br>
Mitigation: Use a separate testnet wallet, confirm the Jovay network before approving transactions, and avoid exposing mainnet private keys. <br>
Risk: Generated contracts and package scripts may contain mistakes or unsafe behavior before review. <br>
Mitigation: Review generated Solidity contracts, frontend code, and package scripts before compiling, testing, deploying, or running them. <br>
Risk: Project scaffolding and dependency installation can execute local development tooling. <br>
Mitigation: Run the workflow in an isolated workspace and inspect dependencies and scripts before executing local servers or install commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryogawan/jovay-dapp) <br>
- [Jovay testnet RPC](https://testnet-rpc.jovay.xyz) <br>
- [Jovay testnet explorer](https://testnet-explorer.jovay.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code blocks, generated project files, shell commands, and configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initialize projects, install dependencies, deploy contracts to testnet, and run a local frontend when the user approves.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata; artifact frontmatter lists 0.0.1alpha) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
