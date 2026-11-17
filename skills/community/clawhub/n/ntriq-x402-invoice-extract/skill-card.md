## Description:

Extract structured invoice data (vendor, line items, totals, tax) from any invoice image. Pay $0.03 USDC via x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ntriq-gh](https://clawhub.ai/user/ntriq-gh)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and finance or accounting workflow builders use this skill to call a paid x402 invoice-extraction service that returns structured invoice or receipt fields from an image URL or base64 input.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoice images or URLs may contain confidential, regulated, customer, tax, banking, or presigned-URL data, and the security evidence flags a conflict between privacy claims and sending inputs to a third-party endpoint.

Mitigation: Use only documents you are authorized to share with the service operator, and confirm privacy, retention, deletion, and compliance terms before using real invoices.

Risk: Each API call is a paid x402 transaction on Base mainnet.

Mitigation: Confirm the $0.03 USDC price, payment network, and payment header handling before enabling automated or high-volume use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ntriq-gh/skills/ntriq-x402-invoice-extract)
- [ntriq x402 service](https://x402.ntriq.co.kr)
- [x402 protocol](https://x402.org)

## Skill Output:

**Output Type(s):** [guidance, shell commands, JSON]

**Output Format:** [Markdown with HTTP request examples, shell commands, and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an image_url or image_base64 input, an x402 payment header, and optionally a language parameter.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
