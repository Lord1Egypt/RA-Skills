## Description:

Call guide and best practices for interacting with a BSC mainnet giveaway contract, including the deployed contract address, core method signatures, parameter meanings, and ethers/web3 calling conventions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[franckstone](https://clawhub.ai/user/franckstone)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to prepare read and write calls for a deployed BSC giveaway contract, including creating giveaways, claiming giveaways, managing whitelists, and withdrawing expired giveaways.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Write calls use a signer on BSC mainnet and can transfer real assets, incur gas and contract fees, and generally cannot be reversed once confirmed.

Mitigation: Prefer read-only checks first and require explicit user confirmation before create, claim, withdraw, approve, or whitelist transactions.

Risk: ERC20 giveaways require token approvals before contract interaction, which can expose assets if the approval target or amount is wrong.

Mitigation: Verify the contract address and approval amount before signing, and keep approvals limited to the intended transaction amount.

## Reference(s):

- [Giveaway Skills on ClawHub](https://clawhub.ai/franckstone/skills/giveaway-skills)
- [Publisher profile: franckstone](https://clawhub.ai/user/franckstone)
- [BSC public RPC endpoint referenced by the skill](https://bsc-dataseed.binance.org)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Solidity, TypeScript, and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance concerns BSC mainnet contract interactions that may require a signer and explicit transaction confirmation.]

## Skill Version(s):

0.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
