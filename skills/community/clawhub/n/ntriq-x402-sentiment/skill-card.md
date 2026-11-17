## Description:

Analyze sentiment, emotions (joy/anger/sadness/fear), and intent from any text. Pay $0.01 USDC via x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ntriq-gh](https://clawhub.ai/user/ntriq-gh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call ntriq's paid x402 sentiment API for sentiment, emotion, intent, confidence, and short-summary analysis of supplied text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The analyzed text is sent to ntriq's external sentiment-analysis service.

Mitigation: Confirm the text is appropriate to share with the external service before calling the API, and avoid sensitive content unless the deployment policy permits it.

Risk: Each API call requires a $0.01 USDC payment through x402 on Base mainnet.

Mitigation: Verify the payment header, network, and expected usage volume before enabling automated calls.

## Reference(s):

- [Ntriq x402 homepage](https://x402.ntriq.co.kr)
- [Ntriq x402 service listing](https://x402.ntriq.co.kr/services)
- [x402 protocol](https://x402.org)
- [ClawHub skill page](https://clawhub.ai/ntriq-gh/skills/ntriq-x402-sentiment)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance with HTTP examples, curl command examples, and JSON response shape]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The external API response includes sentiment, confidence, emotion scores, intent classification, and a one-sentence summary.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
