## Description:

Checks Web3 wallet or transaction security using MetaComp VisionX for supported wallet addresses and transaction hashes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metacompai](https://clawhub.ai/user/metacompai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request KYT security reports for supported Web3 wallets and transactions when a wallet address, transaction hash, or Web3 security concern is provided.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup may run an unpinned npm MCP package under the user's account.

Mitigation: Review the package before installation and prefer a pinned, reviewed package version.

Risk: API tokens can be exposed if placed directly in command configuration.

Mitigation: Configure credentials through METACOMP_TOKEN or a secret manager rather than embedding tokens in command arguments.

Risk: Wallet addresses and transaction details submitted for analysis are sent to MetaComp VisionX.

Mitigation: Submit only data that is acceptable under the user's privacy, compliance, and organizational policies.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/metacompai/skills/metacomp-visionx-kyt)
- [MetaComp Homepage](https://www.metacomp.ai)
- [Skill Homepage](https://github.com/metacomp-ai/remote-mcp)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with tables, inline code, and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include wallet or transaction security reports, cross-vendor risk comparison tables, and configuration steps.]

## Skill Version(s):

1.0.1 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
