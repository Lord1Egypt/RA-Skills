## Description:

Guide users through uploading an image and metadata, mining a vanity salt, and deploying a token on-chain via BondingCurveRouter in a 4-step flow on Nad.fun.

This skill is ready for commercial/non-commercial use.

## Publisher:

[therealharpaljadeja](https://clawhub.ai/user/therealharpaljadeja)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to guide Nad.fun token creation, including image upload, metadata upload, vanity salt mining, and on-chain deployment. It is intended for users who need step-by-step API and smart contract interaction guidance for creating a token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an unpinned wallet-management prerequisite, which could lead users to install or trust the wrong package.

Mitigation: Verify the exact monad-development package and publisher before using it for wallet management or transaction signing.

Risk: The skill can lead to irreversible value-spending blockchain transactions without a required final confirmation step.

Mitigation: Use a dedicated low-balance wallet and require manual confirmation of the contract address, chain, token parameters, fees, initial buy value, and decoded transaction before signing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/therealharpaljadeja/skills/nadfun-token-creation)
- [Nad.fun API Base URL](https://api.nadapp.net)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JavaScript, Solidity, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request bodies, token metadata, wallet-dependent values, contract addresses, fee values, salts, and transaction parameters.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
