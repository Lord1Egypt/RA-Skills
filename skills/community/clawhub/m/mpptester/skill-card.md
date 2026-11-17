## Description:

Runs a Machine Payments Protocol (MPP) conformance test that verifies an agent or wallet can complete a $0.50 USDC payment on Solana and produce a shareable proof.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kris-hansen](https://clawhub.ai/user/kris-hansen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and payment-integration testers use this skill to verify that an agent or wallet can send or receive a Solana USDC payment and publish a shareable proof.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mainnet tests spend real USDC and require SOL fees.

Mitigation: Use devnet for dry runs and confirm intentionally before paying any mainnet Solana Pay request.

Risk: The helper relies on an external payment-testing service and trusts MPP_BASE_URL if it is overridden.

Mitigation: Use the default service URL or only override MPP_BASE_URL with a trusted endpoint.

Risk: Optional labels may be sent to the external service.

Mitigation: Avoid putting secrets, private identifiers, or sensitive customer data in labels.

## Reference(s):

- [MPP Tester Homepage](https://mpptester.com)
- [ClawHub Skill Page](https://clawhub.ai/kris-hansen/skills/mpptester)
- [Solana Pay Documentation](https://docs.solanapay.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with bash, curl, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a Solana Pay URL, polling status, transaction signature, and shareable proof link when the documented flow is run.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata; artifact frontmatter says 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
