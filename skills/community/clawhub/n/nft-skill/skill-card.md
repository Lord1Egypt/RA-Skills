## Description:

Autonomous AI Artist Agent for generating, evolving, minting, listing, and promoting NFT art on the Base blockchain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[numba1ne](https://clawhub.ai/user/numba1ne)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to automate an NFT art workflow: generate or evolve art, upload metadata, mint ERC-721 tokens, list them on a marketplace, monitor sales, and post X/Twitter updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deploy, mint, and list operations can spend wallet funds or create irreversible blockchain transactions.

Mitigation: Use a dedicated low-value wallet, start on Base Sepolia testnet, and require manual approval before deploy, mint, or list commands.

Risk: Marketplace listing may grant broad NFT transfer permissions or use an unintended contract address.

Mitigation: Verify NFT and marketplace contract addresses before use and limit approvals to the intended marketplace whenever possible.

Risk: The skill can post public X/Twitter updates.

Mitigation: Use separate social credentials and require human review before tweet operations.

Risk: Minted NFT metadata may be incomplete or unavailable if IPFS upload does not succeed.

Mitigation: Confirm successful IPFS upload and inspect the returned metadata URI before minting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/numba1ne/skills/nft-skill)
- [Project homepage](https://github.com/Numba1ne/nft-skill)
- [Base network](https://base.org)
- [TypeScript](https://www.typescriptlang.org/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, JSON]

**Output Format:** [JSON command output with shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may create image files, IPFS metadata URIs, blockchain transaction hashes, token IDs, sale events, and X/Twitter post IDs.]

## Skill Version(s):

1.0.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
