## Description:

Batch extract structured data from up to 500 invoices/receipts. Flat $9.00 USDC via x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ntriq-gh](https://clawhub.ai/user/ntriq-gh)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and finance operations teams use this skill to call a paid x402 API that batch extracts structured invoice and receipt fields from image URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoice or receipt image URLs and extracted contents are sent to the provider's remote service.

Mitigation: Use only with documents your organization permits sending to this provider, and review privacy, retention, and compliance terms before using regulated or confidential data.

Risk: The skill requires a flat $9.00 USDC payment through x402 on Base mainnet.

Mitigation: Confirm payment authorization, network, and fee expectations before sending batch requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ntriq-gh/skills/ntriq-x402-invoice-extract-batch)
- [ntriq homepage](https://x402.ntriq.co.kr)
- [Invoice extraction endpoint](https://x402.ntriq.co.kr/invoice-extract-batch)
- [x402 protocol](https://x402.org)
- [Service discovery endpoint](https://x402.ntriq.co.kr/services)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns structured extraction results for invoice or receipt image URLs, including vendor, dates, amounts, currency, and line items when available.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
