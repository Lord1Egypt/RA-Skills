## Description: <br>
Autonomous AI Artist Agent for generating, evolving, minting, listing, and promoting NFT art on the Base blockchain. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Numba1ne](https://clawhub.ai/user/Numba1ne) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and agent users use this skill to generate AI or procedural art, upload metadata to IPFS, mint ERC-721 NFTs on Base, list NFTs for sale, monitor sales, evolve art behavior from sales milestones, and post X/Twitter announcements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent wallet-signing and marketplace authority for minting, listing, and related blockchain actions. <br>
Mitigation: Install with a dedicated low-value wallet, test on Base Sepolia first, and require review of every mint, listing, approval, and transaction before execution. <br>
Risk: The skill can use IPFS, LLM/image providers, and X/Twitter credentials to upload or post externally. <br>
Mitigation: Scope Pinata, LLM/image, and X/Twitter API keys to this project and review generated content before uploads or posts. <br>
Risk: The security scan found no clear human approval gates for mainnet funds, valuable NFTs, or external posting. <br>
Mitigation: Avoid mainnet funds or valuable NFTs unless external spending limits, posting controls, and human approval checks are in place. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Numba1ne/nft-skill) <br>
- [Project homepage](https://github.com/Numba1ne/nft-skill) <br>
- [Base Network](https://base.org) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may sign blockchain transactions, upload NFT metadata to IPFS, stream sales events, and post externally to X/Twitter.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
