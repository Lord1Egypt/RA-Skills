## Description:

Detects phishing URLs and suspicious domains in real time, with risk scoring, brand impersonation detection, and x402 payment per call.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ntriq-gh](https://clawhub.ai/user/ntriq-gh)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and security teams use this skill to submit a URL or domain to a paid phishing-check API and receive risk scoring, indicators, brand impersonation analysis, and a recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted URLs or domains are sent to the provider's external service.

Mitigation: Avoid submitting private internal URLs unless external sharing is acceptable.

Risk: Each use incurs a $0.03 USDC x402 payment.

Mitigation: Confirm payment handling and usage limits before enabling repeated or automated calls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ntriq-gh/skills/ntriq-x402-phish-radar)
- [ntriq homepage](https://x402.ntriq.co.kr)
- [Phish Radar API endpoint](https://x402.ntriq.co.kr/phish-radar)
- [x402 protocol](https://x402.org)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown instructions with shell examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each API call sends the submitted URL or domain to the provider's external service and costs $0.03 USDC via x402.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
