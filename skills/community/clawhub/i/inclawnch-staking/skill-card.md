## Description:

Stake and unstake INCLAWNCH tokens in the on-chain UBI staking contract on Base, query treasury stats, wallet positions, APY estimates, and top stakers, with write operations requiring wallet-signed on-chain transactions and reads using a public API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stuart5915](https://clawhub.ai/user/stuart5915)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to inspect INCLAWNCH staking data, prepare staking, unstaking, claiming, and auto-compound actions, and understand wallet-signed transactions on Base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet-signed approval, staking, claiming, auto-compound, and exit actions can affect on-chain assets.

Mitigation: Review the token and staking contract addresses carefully in the wallet before signing, and sign only when the user trusts the contract and understands the transaction.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/stuart5915/skills/inclawnch-staking)
- [Inclawbate Skills Directory](https://inclawbate.com/skills)
- [Machine-Readable Staking Skill Spec](https://inclawbate.com/api/inclawbate/skill/staking)
- [Staking Read Endpoint](https://inclawbate.com/api/inclawbate/staking)
- [UBI Dashboard](https://inclawbate.com/ubi)
- [BaseScan Token Contract](https://basescan.org/token/0xB0b6e0E9da530f68D713cC03a813B506205aC808)
- [BaseScan Staking Contract](https://basescan.org/address/0x206C97D4Ecf053561Bd2C714335aAef0eC1105e6)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with curl examples and on-chain transaction parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for public API examples; wallet-signed transactions are required for write operations.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
