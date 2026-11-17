## Description:

Ntriq X402 Compliance Check analyzes contracts, policies, and text for compliance issues, detects risks, and recommends fixes through a paid x402 API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ntriq-gh](https://clawhub.ai/user/ntriq-gh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to submit contracts, policies, or plain text to the Ntriq x402 compliance-check API and receive compliance status, issue severity, and remediation guidance for frameworks such as GDPR, HIPAA, SOX, general corporate policy, or custom frameworks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Each use sends analyzed text to an external service.

Mitigation: Do not submit contracts, policies, regulated data, or other sensitive content unless the external service provider is approved for the use case.

Risk: Each compliance check costs $0.03 USDC through an x402 payment flow.

Mitigation: Confirm the payment network, price, and payer authorization before invoking the API.

## Reference(s):

- [Ntriq x402 homepage](https://x402.ntriq.co.kr)
- [Ntriq compliance-check API](https://x402.ntriq.co.kr/compliance-check)
- [x402 protocol](https://x402.org)
- [Ntriq services endpoint](https://x402.ntriq.co.kr/services)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include compliance status, risk level, issue descriptions, severity, summaries, and remediation recommendations.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
