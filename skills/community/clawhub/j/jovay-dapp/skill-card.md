## Description:

Full-stack dApp generation skill for Jovay blockchain - from requirements gathering to contract deployment and frontend debugging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryogawan](https://clawhub.ai/user/ryogawan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to gather dApp requirements, scaffold Jovay blockchain projects, generate Solidity contracts and Vue 3 frontends, and guide testnet deployment and debugging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run npm-based installations and remote template scaffolding.

Mitigation: Inspect generated template files and package scripts before installing dependencies or running project commands; pin package versions where possible.

Risk: The workflow may involve wallet secrets or encryption keys in local blockchain deployment commands.

Mitigation: Use a fresh low-value testnet wallet and avoid entering private keys or encryption keys directly into shell commands.

Risk: Generated contracts and frontends may contain defects or unsafe assumptions for production use.

Mitigation: Review and test generated code before deployment, and keep deployment to testnet unless production readiness has been separately established.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryogawan/skills/jovay-dapp)
- [jovay-cli npm package](https://www.npmjs.com/package/@jovaylabs/jovay-cli)
- [Jovay testnet RPC](https://testnet-rpc.jovay.xyz)
- [Jovay testnet explorer](https://testnet-explorer.jovay.xyz)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with code blocks and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create smart contracts, frontend files, deployment configuration, and local development commands.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
