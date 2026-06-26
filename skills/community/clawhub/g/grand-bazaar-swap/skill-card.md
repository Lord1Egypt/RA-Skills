## Description: <br>
Perform and document Grand Bazaar P2P swaps on Base using deployed AirSwap Swap contracts, including workflows for approvals, EIP-712 signing, cast/deeplink posting, execution, and verification across ERC20, ERC721, and ERC1155 routes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agriimony](https://clawhub.ai/user/agriimony) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external agents use this skill to create, publish, take, and verify Grand Bazaar P2P swap orders on Base mainnet. It supports signer and sender workflows for AirSwap-style orders, including pricing parameters, Farcaster order transport, approvals, execution, and transaction verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can approve token spending and execute real Base mainnet trades. <br>
Mitigation: Use isolated low-value wallets and verify the chain, token addresses, swap contract, recipient, amounts, fees, expiry, and approvals before any transaction. <br>
Risk: Scripts can operate with raw private keys and do not provide strong built-in confirmation controls before approval, signing, casting, or swap broadcast. <br>
Mitigation: Require explicit operator confirmation before each approval, EIP-712 signature, Farcaster post, or onchain swap execution. <br>


## Reference(s): <br>
- [Base mainnet deployments](references/base-mainnet-deployments.md) <br>
- [Size-Aware OTC Pricing Parameters](references/pricing-params.md) <br>
- [Grand Bazaar Swap scripts](scripts/README.md) <br>
- [Grand Bazaar Swap on ClawHub](https://clawhub.ai/agriimony/grand-bazaar-swap) <br>
- [AirSwap Web order route](https://dex.airswap.xyz/#/order/) <br>
- [Grand Bazaar miniapp](https://the-grand-bazaar.vercel.app/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with JavaScript scripts, shell commands, and JSON order or cast payloads.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce compressed GBZ1 order payloads, approval or swap transaction instructions, and Base transaction hashes that require operator review before broadcast.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
