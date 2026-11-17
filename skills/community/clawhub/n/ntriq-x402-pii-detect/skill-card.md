## Description:

Detect and optionally mask PII (emails, phone numbers, SSNs, names, addresses, credit cards) in text. Pay $0.02 USDC via x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ntriq-gh](https://clawhub.ai/user/ntriq-gh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to submit text to ntriq's paid x402 API for PII detection, risk scoring, positional findings, and optional masking before sharing or storing text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted text is sent to ntriq's remote service for processing.

Mitigation: Avoid regulated, confidential, or customer data unless the provider's privacy, retention, logging, and compliance terms satisfy the intended use.

Risk: The API is payment-gated through x402.

Mitigation: Confirm the endpoint, Base mainnet payment flow, and per-call USDC cost before automated or high-volume use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ntriq-gh/skills/ntriq-x402-pii-detect)
- [ntriq x402 service homepage](https://x402.ntriq.co.kr)
- [x402 protocol](https://x402.org)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with HTTP examples and JSON request/response structures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [API responses include detected PII types, character positions, risk level, and optional masked text.]

## Skill Version(s):

1.0.0 (source: evidence release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
