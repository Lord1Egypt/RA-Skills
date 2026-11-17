## Description:

Batch compliance analysis for up to 500 texts with flat $9.00 USDC payment via x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ntriq-gh](https://clawhub.ai/user/ntriq-gh)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and compliance teams use this skill to submit batches of text for compliance review against frameworks such as GDPR, HIPAA, SOX, or a general policy setting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted compliance texts may be sent to a remote paid third-party service.

Mitigation: Do not submit confidential, regulated, customer, employee, health, legal, or proprietary content unless the provider and its privacy, logging, retention, and payment practices have been reviewed.

Risk: The artifact claims local inference while the skill behavior requires using a remote service endpoint.

Mitigation: Treat the service as remote processing unless the provider's deployment and data-handling claims have been independently confirmed.

## Reference(s):

- [Ntriq x402 homepage](https://x402.ntriq.co.kr)
- [x402 protocol](https://x402.org)
- [ClawHub skill page](https://clawhub.ai/ntriq-gh/skills/ntriq-x402-compliance-check-batch)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with API request examples and parameter guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May involve paid x402 requests to a remote third-party service.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
