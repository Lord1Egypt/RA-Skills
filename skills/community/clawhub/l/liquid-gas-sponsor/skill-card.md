## Description:

Send any transaction on Base with a wallet that holds USDC but no ETH. Pay the gas per operation in USDC over x402 (from $0.03) through an ERC-4337 paymaster; one endpoint for smart-wallet SDKs and plain wallets. No account, no API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leftychris13](https://clawhub.ai/user/leftychris13)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents that manage Base wallets use this skill to prepare sponsored transactions when a wallet holds USDC but no ETH. It provides guidance for plain wallets, existing smart accounts, and ERC-7677 smart-wallet SDK paymaster flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents through real Base wallet payments and signed on-chain submissions.

Mitigation: Require manual review and approval of chain ID, target contract, calldata purpose, USDC fee, payment recipient, and signed typed data before any payment or signature.

Risk: EIP-7702 delegation or redelegation can change the wallet implementation used for execution.

Mitigation: Review any authorization and confirm the delegation or redelegation target before signing; do not allow automatic redelegation.

Risk: The sponsorship fee is taken at sponsorship time even when the on-chain operation later fails.

Mitigation: Build and simulate calls before requesting sponsorship, and refresh expired quotes rather than reusing stale transaction data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leftychris13/skills/liquid-gas-sponsor)
- [Liquid Gas Sponsor API](https://api.liquidagent.ai/v1/gas)
- [Liquid Gas Sponsor usage stats](https://api.liquidagent.ai/v1/gas/stats)
- [Gasless bring-your-own-operation example](https://github.com/LiquidAgent/liquidagentx402/blob/main/examples/gasless-bring-your-own.js)
- [Gasless transaction example](https://github.com/LiquidAgent/liquidagentx402/blob/main/examples/gasless.js)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for command examples; no API key or account is described.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
