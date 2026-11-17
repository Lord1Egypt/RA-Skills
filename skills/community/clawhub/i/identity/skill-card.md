## Description:

Know Your Agent (KYA). Billions decentralized identity for agents. Link agents to human identities using Billions ERC-8004 and Attestation Registries. Verify and generate authentication proofs. Based on iden3 self-sovereign identity protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billionsnetwork](https://clawhub.ai/user/billionsnetwork)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create, manage, link, prove, and verify decentralized identities for AI agents. It also helps agents handle x402 payment-required responses by presenting payment options for explicit user confirmation and generating signed payment requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private identity keys may be stored insecurely when the master key environment variable is not configured.

Mitigation: Set BILLIONS_NETWORK_MASTER_KMS_KEY before creating or importing an identity and restrict ~/.openclaw/billions permissions to the local operator.

Risk: Reusing an asset-holding Ethereum wallet key could expand the impact of key disclosure beyond agent identity impersonation.

Mitigation: Use only a dedicated no-funds identity key for this skill.

Risk: The x402 payment flow can sign payment requests after user selection, so a misleading destination, recipient, asset contract, network, or amount could cause unintended payment.

Mitigation: Use the payment flow only after independently verifying the destination, recipient, asset contract, network, amount, and user consent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/billionsnetwork/skills/identity)
- [Billions Network](https://billions.network/)
- [Artifact README](artifact/README.md)
- [Security Policy](artifact/SECURITY.md)
- [Identity Reference](artifact/reference/identity/SKILL.md)
- [x402 Payment Reference](artifact/reference/x402/SKILL.md)
- [OpenClaw environment documentation](https://docs.openclaw.ai/help/environment)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown and text guidance with inline shell commands, JSON script output, DID strings, verification URLs, and payment-signature flow data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include local identity records, authentication proofs, signed challenge results, and x402 payment option data that requires explicit user confirmation before payment execution.]

## Skill Version(s):

2.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
