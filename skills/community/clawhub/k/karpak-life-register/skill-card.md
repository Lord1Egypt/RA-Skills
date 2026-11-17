## Description:

Automates Karpak Life registration and Soulbound Token minting on the Karpak Living Map when a user asks to register or mint an SBT.

This skill is ready for commercial/non-commercial use.

## Publisher:

[karpak-developer](https://clawhub.ai/user/karpak-developer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide an agent through Karpak Life wallet registration and Soulbound Token minting on BSC testnet or mainnet with MetaMask-compatible wallet approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects a browser wallet and requests a signature.

Mitigation: Confirm wallet prompts manually and reject unexpected signature requests; verify the selected environment before signing.

Risk: The skill may request a gas-spending BSC mainnet mint transaction.

Mitigation: Choose testnet or mainnet explicitly and review transaction details, destination, and gas before confirming.

Risk: The local wallet bridge is unauthenticated and allows cross-origin requests.

Mitigation: Run only in a trusted local browser session, close the bridge after use, and prefer a release with per-session bridge token and origin checks.

Risk: Wallet and profile data is sent to Karpak and SBT services.

Mitigation: Use wallet and profile details appropriate for registration and avoid sharing unnecessary personal information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/karpak-developer/skills/karpak-life-register)
- [Karpak Life API mainnet endpoint](https://lifestyle-api.karpak.xyz)
- [Karpak SBT mainnet endpoint](https://sbt.karpak.xyz)
- [Karpak Life API testnet endpoint](https://devnet-lifestyle-api.karpak.xyz)
- [Karpak SBT testnet endpoint](https://devnet.paratrix-sbt.pages.dev)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include wallet address, registration status, credential state, transaction hash, and explorer URL.]

## Skill Version(s):

1.0.6 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
