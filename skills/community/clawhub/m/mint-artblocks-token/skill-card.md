## Description:

Mint or prepare to purchase an Art Blocks token using artblocks-mcp tools, including project discovery, minter configuration, eligibility checks, pricing, and transaction preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryley-o](https://clawhub.ai/user/ryley-o)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to guide Art Blocks minting workflows, inspect live minter details, check gated eligibility, and prepare supported ETH set-price purchase transactions before wallet signing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A prepared NFT mint transaction may target the wrong project, chain, price, or recipient if inputs are not checked before signing.

Mitigation: Review the project, chain, price, recipient address, warnings, and gas cost in the wallet before signing.

Risk: Eligibility checks for an Art Blocks username may query all wallets linked to that profile.

Mitigation: Use a single wallet address for eligibility checks when the user does not want profile-linked wallets queried together.

Risk: Some minter and currency types are not supported by the transaction builder.

Mitigation: Use the skill to explain unsupported minter mechanics and direct the user to their wallet rather than preparing an unsupported transaction.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, API Calls, configuration]

**Output Format:** [Markdown guidance with structured tool parameters and transaction-preparation details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Surfaces project, minter, price, eligibility, chain, recipient, and warning details; only supports transaction building for MinterSetPriceV5 ETH purchases.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
