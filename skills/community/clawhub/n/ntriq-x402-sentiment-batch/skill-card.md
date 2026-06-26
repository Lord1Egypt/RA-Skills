## Description: <br>
Batch sentiment and intent analysis for up to 500 texts. Flat $3.00 USDC via x402. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ntriq-gh](https://clawhub.ai/user/ntriq-gh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to submit batches of text to a paid x402 sentiment-analysis endpoint and receive sentiment, confidence, intent, and summary results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Each API call may spend $3.00 USDC through the x402 payment flow. <br>
Mitigation: Use explicit payment approval or a limited wallet before allowing an agent to call the endpoint. <br>
Risk: Submitted texts are sent to a remote third-party service. <br>
Mitigation: Avoid submitting secrets, regulated data, or sensitive personal or business content unless the provider is trusted for that data. <br>


## Reference(s): <br>
- [Ntriq x402 Service](https://x402.ntriq.co.kr) <br>
- [Sentiment Batch Endpoint](https://x402.ntriq.co.kr/sentiment-batch) <br>
- [x402 Protocol](https://x402.org) <br>
- [ClawHub Skill Listing](https://clawhub.ai/ntriq-gh/ntriq-x402-sentiment-batch) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote API responses are JSON sentiment results; calls require x402 payment headers.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
