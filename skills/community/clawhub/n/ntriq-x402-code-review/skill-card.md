## Description:

AI code review for security, performance, and quality. Returns scored issues and suggestions. $0.05 USDC via x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ntriq-gh](https://clawhub.ai/user/ntriq-gh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to submit code snippets to ntriq's paid remote review service for security, performance, and quality feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted code snippets are sent to ntriq's external service and may contain secrets, credentials, private keys, personal data, or proprietary material.

Mitigation: Review snippets before submission, remove sensitive material, and use the service only with appropriate approval and data-handling assurances.

Risk: The skill uses a paid x402 flow that requires authorizing the stated payment.

Mitigation: Confirm the $0.05 USDC charge, payment header, and Base mainnet payment flow before each call or integration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ntriq-gh/skills/ntriq-x402-code-review)
- [ntriq x402 homepage](https://x402.ntriq.co.kr)
- [x402 protocol](https://x402.org)
- [ntriq services endpoint](https://x402.ntriq.co.kr/services)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Shell commands]

**Output Format:** [Markdown with JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a scored review with prioritized issues, security risks, summaries, and actionable suggestions from the remote service.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
