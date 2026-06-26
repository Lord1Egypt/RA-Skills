## Description: <br>
Batch phishing detection for up to 500 URLs or domains. Flat $9.00 USDC via x402. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ntriq-gh](https://clawhub.ai/user/ntriq-gh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit batches of URLs or domains to a paid phishing-scan API and receive per-target risk levels and visit/block recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid requests can spend USDC through the x402 payment flow. <br>
Mitigation: Confirm paid requests before sending them and use wallet limits appropriate for the expected scan volume. <br>
Risk: Submitted URLs or domains may reveal private investigations, internal systems, or sensitive targets to the provider. <br>
Mitigation: Avoid submitting private internal URLs or sensitive investigation targets unless the provider is trusted with that data. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/ntriq-gh/ntriq-x402-phish-radar-batch) <br>
- [Ntriq homepage](https://x402.ntriq.co.kr) <br>
- [Phish Radar Batch API endpoint](https://x402.ntriq.co.kr/phish-radar-batch) <br>
- [x402 protocol](https://x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Analysis, Guidance] <br>
**Output Format:** [JSON response with per-target phishing risk levels and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts up to 500 URLs or domains per paid request.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
