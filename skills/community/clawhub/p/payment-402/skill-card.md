## Description:

Access protected APIs and digital resources via the x402 Payment Required protocol on Base L2 by automating cryptographic handshakes and USDC micro-payments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paynodelabs](https://clawhub.ai/user/paynodelabs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to check wallet readiness, complete x402 payment challenges, and retrieve protected API resources that require USDC payment on Base networks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically sign blockchain payments with a raw private key, and spending safeguards are documented but not enforced in code.

Mitigation: Use only a dedicated burner wallet with funds the operator is willing to risk, prefer testnet first, and add code-level spend limits or allowlists before autonomous use.

Risk: Any request URL may become payment-capable, creating risk of payment to an unexpected merchant or for an unexpected amount.

Mitigation: Verify the merchant, requested resource, network, and expected amount before first payment, and require human approval for higher-value or unfamiliar transactions.

## Reference(s):

- [Sandbox & Testing](references/TESTING.md)
- [PayNode Documentation](https://github.com/PayNodeLabs/paynode-docs)
- [PayNode Hub](https://github.com/PayNodeLabs/paynode-web)
- [Base Sepolia MockUSDC Contract](https://sepolia.basescan.org/address/0x109AEddD656Ed2761d1e210E179329105039c784#writeContract)
- [ClawHub Skill Page](https://clawhub.ai/paynodelabs/skills/payment-402)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Bun and CLIENT_PRIVATE_KEY; can call payment-protected HTTP endpoints and return retrieved resource data.]

## Skill Version(s):

1.0.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
