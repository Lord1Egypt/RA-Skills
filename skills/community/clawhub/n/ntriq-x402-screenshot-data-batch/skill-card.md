## Description:

Batch extract text, UI elements, and data from up to 500 screenshots. Flat $6.00 USDC via x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ntriq-gh](https://clawhub.ai/user/ntriq-gh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to submit authorized screenshot URLs to a paid third-party x402 endpoint and receive batched extraction of text, UI elements, layout structure, and data tables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screenshots and extracted data are sent to a third-party service.

Mitigation: Submit only screenshots you are authorized to share, and redact credentials, customer data, internal dashboards, personal information, and regulated data before use.

Risk: The workflow requires an x402 payment for a flat $6.00 USDC request.

Mitigation: Confirm the endpoint, network, payment amount, and x402 payment header before sending a request.

## Reference(s):

- [Ntriq homepage](https://x402.ntriq.co.kr)
- [x402 protocol](https://x402.org)
- [ClawHub skill page](https://clawhub.ai/ntriq-gh/skills/ntriq-x402-screenshot-data-batch)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands, Guidance]

**Output Format:** [Markdown instructions with HTTP examples and JSON response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts up to 500 screenshot URLs with optional extract_type and language parameters.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
