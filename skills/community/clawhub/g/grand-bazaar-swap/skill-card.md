## Description:

Perform and document Grand Bazaar P2P swaps on Base using deployed AirSwap Swap contracts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agriimony](https://clawhub.ai/user/agriimony)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to create, publish, validate, and execute two-party Grand Bazaar swap orders on Base mainnet across ERC20, ERC721, and ERC1155 routes. It supports signer-side order construction, sender-side execution, Farcaster cast payloads, and verification steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill targets real Base mainnet swaps and its scripts can approve and move assets when raw private keys are supplied.

Mitigation: Use dedicated low-value wallets, start with tiny amounts, keep production private keys out of shell environments, and review every approval and transaction before broadcast.

Risk: Order metadata can influence the swap contract target and token amounts used by execution scripts.

Mitigation: Only execute orders whose swap contract is allowlisted, independently verify token and contract addresses, and confirm transaction details before running sender execution.

Risk: Dependency and runtime behavior may change over time for wallet, RPC, or transaction tooling.

Mitigation: Pin and review dependencies, apply dependency updates deliberately, and add a dry-run or explicit confirmation gate before production operation.

## Reference(s):

- [Grand Bazaar Swap on ClawHub](https://clawhub.ai/agriimony/skills/grand-bazaar-swap)
- [Base mainnet deployments](references/base-mainnet-deployments.md)
- [Size-Aware OTC Pricing Parameters](references/pricing-params.md)
- [Scripts README](scripts/README.md)
- [AirSwap Web order URL](https://dex.airswap.xyz/#/order/)
- [Grand Bazaar Miniapp](https://the-grand-bazaar.vercel.app/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with inline shell commands, JavaScript reference scripts, and JSON order or cast payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Base mainnet transaction preparation and execution guidance; script outputs can include order JSON, compressed order strings, cast payload JSON, transaction hashes, and balance or gas summaries.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
