## Description:

Batch operations for NEAR tokens - send to multiple recipients, transfer NFTs, claim rewards with cost estimation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaiss](https://clawhub.ai/user/shaiss)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to prepare, estimate, and run batch NEAR token sends and NFT transfers from JSON input files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch send and NFT transfer operations can move real assets in bulk.

Mitigation: Verify every account, amount, contract, token ID, and network context before execution; use a controlled environment and dry-run or confirmation flow for valuable assets.

Risk: The script runs unvalidated shell commands from user-supplied JSON.

Mitigation: Audit input JSON before use and prefer updating the script to use argument-array process execution, validation, and batch limits.

## Reference(s):

- [NEAR CLI](https://docs.near.org/tools/near-cli)
- [NEAR Batch Actions](https://docs.near.org/api/rpc/transactions/batch-actions)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NEAR CLI configuration and sufficient account balance for transfer operations.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
