## Description: <br>
Buy and sell NFTs on OpenSea's Seaport marketplace by fulfilling listings, accepting offers, creating orders, making cross-chain purchases, and sweeping multiple listings, with wallet signing required and read-only queries routed to opensea-api. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[opensea](https://clawhub.ai/user/opensea) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and agents use this skill to execute OpenSea marketplace workflows for NFTs, including listing fulfillment, offer acceptance, cross-chain purchases, and multi-listing sweeps. It is appropriate when wallet-backed signing and transaction review are part of the workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Marketplace workflows can produce live transactions that move assets or grant token approvals. <br>
Mitigation: Use a dedicated low-balance wallet, prefer managed signers with spending caps and allowlists, and review every transaction before signing. <br>
Risk: Fulfillment responses and transaction payloads may include targets, values, or calldata that are unsafe, stale, or unexpected. <br>
Mitigation: Verify the transaction target, value, calldata, order hash, chain, and approval steps before submitting any transaction. <br>
Risk: API keys, wallet credentials, cached keys, or raw private keys could expose trading authority. <br>
Mitigation: Store credentials only in environment variables, avoid raw private keys except for local development, and clean up cached keys or tokens when no longer needed. <br>


## Reference(s): <br>
- [OpenSea Marketplace API](opensea-marketplace/references/marketplace-api.md) <br>
- [Seaport Protocol Reference](opensea-marketplace/references/seaport.md) <br>
- [OpenSea Skill Repository](https://github.com/ProjectOpenSea/opensea-skill) <br>
- [OpenSea CLI](https://github.com/ProjectOpenSea/opensea-cli) <br>
- [OpenSea Developer Docs](https://docs.opensea.io/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, API Calls] <br>
**Output Format:** [Markdown with inline bash commands, API request examples, JSON payloads, and transaction guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include transaction calldata or ordered transaction steps that require wallet review and signing before onchain submission.] <br>

## Skill Version(s): <br>
2.16.0 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
