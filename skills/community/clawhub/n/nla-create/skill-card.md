## Description:

Create a Natural Language Agreement escrow on-chain by gathering escrow parameters, helping craft an AI-arbitrated natural-language demand, and running the nla CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mlegls](https://clawhub.ai/user/mlegls)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to create on-chain ERC20 escrows whose release condition is written as a natural-language demand and evaluated by an AI oracle.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet private keys or signing credentials may be exposed through chat, command-line flags, or environment variables.

Mitigation: Use a dedicated low-value wallet and avoid pasting private keys into chat or command lines.

Risk: Incorrect network, token, amount, oracle, or transaction details can create unsafe or unintended blockchain transactions.

Mitigation: Independently confirm the network, token contract, amount, oracle address, and transaction details before signing.

Risk: Running an unverified nla CLI package can introduce supply-chain or execution risk.

Mitigation: Verify the nla package source and version before installing or using it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mlegls/skills/nla-create)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include the escrow UID returned by nla escrow:create and next-step guidance for fulfillment and collection.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter metadata version 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
