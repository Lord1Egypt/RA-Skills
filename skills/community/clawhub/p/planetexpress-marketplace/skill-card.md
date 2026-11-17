## Description:

Decentralized file marketplace on Monad blockchain - buy, sell, and browse encrypted files with x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timowhite88](https://clawhub.ai/user/timowhite88)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agents use this skill to browse marketplace listings, purchase encrypted files, and list files for sale through x402 payment flows on Monad, Solana, and Base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents toward real blockchain purchases, listing fees, or transaction submissions.

Mitigation: Require explicit human approval before any purchase, listing fee, or transaction submission, and verify network, price, recipient, and listing details before payment.

Risk: Marketplace files and skill files may be untrusted content.

Mitigation: Treat downloaded files as untrusted and review or sandbox them before opening, decrypting, executing, or installing related content.

Risk: SDK installation commands may alter the agent runtime environment.

Mitigation: Pin SDK versions and install them only in an isolated environment intended for marketplace interaction.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/timowhite88/skills/planetexpress-marketplace)
- [Planet Express Marketplace Frontend](https://planetexpress.dropclaw.cloud)
- [DropClaw Marketplace API](https://dropclaw.cloud/marketplace)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration]

**Output Format:** [Markdown with HTTP examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents through network requests, x402 payment retries, and SDK installation commands.]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact/claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
