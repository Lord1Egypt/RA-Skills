## Description:

Cross-chain token swaps and bridges via the LI.FI protocol. Get quotes, execute transfers, track progress, and compose DeFi operations across 35+ blockchains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rhlsthrm](https://clawhub.ai/user/rhlsthrm)

### License/Terms of Use:


## Use Case:

Developers and external agent users use this skill to request LI.FI quotes, compare cross-chain routes, prepare swap or bridge transaction data, track transfers, and compose DeFi zaps across supported chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Returned transactionRequest data can initiate real blockchain transactions that move funds.

Mitigation: Verify chain, token, address, amount, slippage, fees, route, contract calls, and ERC20 allowance in the wallet before signing.

Risk: LI.FI receives wallet and transaction details needed to quote or track transfers.

Mitigation: Use the skill only when sharing those details with the LI.FI API is acceptable for the user and transaction.

Risk: Cross-chain bridges are non-atomic and transfers may remain pending, partially complete, fail, or refund.

Mitigation: Review the route summary before execution and track the transfer status after submitting the source-chain transaction.

## Reference(s):

- [ClawHub Listing](https://clawhub.ai/rhlsthrm/skills/lifi-crosschain)
- [LI.FI Documentation](https://docs.li.fi)
- [LI.FI API Reference](https://apidocs.li.fi)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and transaction request summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include LI.FI API responses, route comparisons, transfer status summaries, and wallet-ready transactionRequest data for user review before signing.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
