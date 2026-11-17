## Description:

Batch detect and mask PII across up to 500 text inputs. Flat $6.00 USDC via x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ntriq-gh](https://clawhub.ai/user/ntriq-gh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and privacy, compliance, or security teams use this skill to call a paid batch service that detects PII in text and can request masked output. It is intended for authorized review of up to 500 text inputs per batch.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw sensitive text is sent to a third-party remote service before masking.

Mitigation: Use only with text you are authorized to send, and confirm the provider's privacy, retention, deletion, logging, and data-processing terms before processing personal, customer, employee, financial, health, or regulated data.

Risk: The API requires a paid x402 payment header.

Mitigation: Confirm the $6.00 USDC charge, Base mainnet network, and recipient/payment details before attaching a payment header or automating requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ntriq-gh/skills/ntriq-x402-pii-detect-batch)
- [ntriq x402 service homepage](https://x402.ntriq.co.kr)
- [PII detect batch API endpoint](https://x402.ntriq.co.kr/pii-detect-batch)
- [ntriq services endpoint](https://x402.ntriq.co.kr/services)
- [x402 protocol](https://x402.org)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown with HTTP, bash, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The remote API returns per-input PII findings, risk level, and optional masked text.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
