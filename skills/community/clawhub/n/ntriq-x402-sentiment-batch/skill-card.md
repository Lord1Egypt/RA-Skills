## Description:

Batch sentiment and intent analysis for up to 500 texts. Flat $3.00 USDC via x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ntriq-gh](https://clawhub.ai/user/ntriq-gh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to send batches of text to ntriq's remote sentiment-analysis endpoint and receive sentiment, confidence, emotion, intent, and summary information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Texts submitted for analysis are sent to ntriq's remote service.

Mitigation: Do not submit secrets, regulated content, private customer data, or confidential business text unless the provider is authorized to handle it.

Risk: The x402 payment header is sent to the remote service.

Mitigation: Review payment authorization and endpoint details before making requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ntriq-gh/skills/ntriq-x402-sentiment-batch)
- [Publisher profile](https://clawhub.ai/user/ntriq-gh)
- [ntriq x402 homepage](https://x402.ntriq.co.kr)
- [x402 protocol](https://x402.org)
- [ntriq services endpoint](https://x402.ntriq.co.kr/services)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, JSON]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces request guidance for a paid remote API that returns per-text sentiment, confidence, intent, and summary fields.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
