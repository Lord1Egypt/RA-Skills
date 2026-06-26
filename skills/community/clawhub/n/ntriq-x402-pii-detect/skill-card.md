## Description: <br>
Detect and optionally mask PII (emails, phone numbers, SSNs, names, addresses, credit cards) in text. Pay $0.02 USDC via x402. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ntriq-gh](https://clawhub.ai/user/ntriq-gh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to send text to a paid remote PII detection service, receive detected PII types with positions and risk level, and optionally return masked text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted text may contain sensitive personal, regulated, or confidential data and is sent to x402.ntriq.co.kr. <br>
Mitigation: Submit only data that is necessary for the task, and review the provider's privacy, retention, and compliance terms before using regulated or confidential content. <br>
Risk: Each call requires a $0.02 USDC x402 payment. <br>
Mitigation: Confirm payment authorization and expected usage volume before integrating the service into automated workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ntriq-gh/ntriq-x402-pii-detect) <br>
- [Publisher profile](https://clawhub.ai/user/ntriq-gh) <br>
- [Service homepage](https://x402.ntriq.co.kr) <br>
- [PII detection endpoint](https://x402.ntriq.co.kr/pii-detect) <br>
- [x402 protocol](https://x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Markdown instructions with HTTP examples and JSON response data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include detected PII values, character positions, risk level, and masked text when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
