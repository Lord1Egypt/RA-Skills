## Description:

Gnosis Safe / multisig treasury setup, monitoring, and governance for DAOs and crypto treasuries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

External DAO operators, protocol teams, and crypto treasury managers use this skill to set up and monitor multisig treasuries, manage signers, prepare spending proposals, and produce treasury health reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Treasury guidance could be mistaken for authorization to execute transactions or handle signer keys.

Mitigation: Keep private keys and signing decisions outside the agent, and require explicit human approval for every Safe transaction.

Risk: Incorrect Safe addresses, thresholds, or emergency signer-removal steps could lead to failed governance actions or loss of funds.

Mitigation: Independently verify addresses, thresholds, signer ownership, and emergency procedures before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samledger67-dotcom/skills/multi-sig-treasury)
- [Publisher profile](https://clawhub.ai/user/samledger67-dotcom)
- [Safe transaction service API: Safe info](https://safe-transaction-mainnet.safe.global/api/v1/safes/0xYOUR_SAFE_ADDRESS/)
- [Safe transaction service API: transactions](https://safe-transaction-mainnet.safe.global/api/v1/safes/0xYOUR_SAFE_ADDRESS/all-transactions/)
- [Safe transaction service API: balances](https://safe-transaction-mainnet.safe.global/api/v1/safes/0xYOUR_SAFE_ADDRESS/balances/usd/)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with checklists, templates, configuration snippets, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance only; it does not execute live on-chain transactions.]

## Skill Version(s):

1.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
