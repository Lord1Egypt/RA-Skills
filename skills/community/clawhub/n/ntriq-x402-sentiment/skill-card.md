## Description: <br>
Analyze sentiment, emotions (joy/anger/sadness/fear), and intent from any text. Pay $0.01 USDC via x402. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ntriq-gh](https://clawhub.ai/user/ntriq-gh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to submit text for paid sentiment, emotion, and intent analysis through the ntriq x402 API. It is suited for workflows that need structured sentiment labels, confidence, emotion scores, intent classification, and a short summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for analysis is sent to a third-party API endpoint. <br>
Mitigation: Do not submit secrets, credentials, regulated personal data, or confidential business text unless the provider's data handling is approved for that data. <br>
Risk: Each API call initiates a paid x402 request using USDC on Base mainnet. <br>
Mitigation: Confirm the $0.01 USDC cost, payment header, wallet, and network before enabling automated or repeated calls. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ntriq-gh/ntriq-x402-sentiment) <br>
- [ntriq x402 Homepage](https://x402.ntriq.co.kr) <br>
- [ntriq Sentiment Endpoint](https://x402.ntriq.co.kr/sentiment) <br>
- [x402 Protocol](https://x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Analysis, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON sentiment response with Markdown and shell command usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires text input, optional language code, and an x402 payment header; each request costs $0.01 USDC on Base mainnet.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
