## Description:

Batch document OCR, classification, and extraction for up to 500 images. Flat $15.00 USDC via x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ntriq-gh](https://clawhub.ai/user/ntriq-gh)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators use this skill to submit batches of document image URLs for paid OCR, classification, table extraction, extraction, and summarization through the provider's x402-enabled API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document image URLs and extracted content are shared with the provider's remote service.

Mitigation: Submit only documents you are authorized to share, and avoid confidential, regulated, or third-party materials unless the provider's retention and privacy practices are acceptable.

Risk: Each batch call requires a $15 USDC x402 payment.

Mitigation: Confirm payment intent, network, and batch contents before sending the request.

## Reference(s):

- [Ntriq service homepage](https://x402.ntriq.co.kr)
- [Document intelligence batch API endpoint](https://x402.ntriq.co.kr/document-intel-batch)
- [x402 protocol](https://x402.org)
- [ClawHub skill page](https://clawhub.ai/ntriq-gh/skills/ntriq-x402-document-intel-batch)

## Skill Output:

**Output Type(s):** [API Calls, Analysis, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with HTTP and curl examples; service responses are JSON containing document analysis text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts up to 500 document image URLs per request and supports extract, summarize, classify, and table analysis modes.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
