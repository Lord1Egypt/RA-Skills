## Description: <br>
Real-time phishing detection for URLs and domains, with risk scoring, brand impersonation detection, and paid x402 access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ntriq-gh](https://clawhub.ai/user/ntriq-gh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit URLs or domains for phishing and suspicious-domain analysis before deciding whether to allow, warn on, or block a target. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted URLs or domains are sent to Ntriq for analysis and may expose sensitive internal resources, secrets, or session tokens if users provide private links. <br>
Mitigation: Submit only URLs or domains that are appropriate to share with Ntriq; strip secrets, session tokens, and internal-only resource identifiers before use. <br>
Risk: Each API request is a paid x402 transaction and repeated automated calls could create unintended charges. <br>
Mitigation: Use wallet, spending, and agent controls to limit repeated calls and confirm that paid requests are intentional. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ntriq-gh/ntriq-x402-phish-radar) <br>
- [Publisher Profile](https://clawhub.ai/user/ntriq-gh) <br>
- [Ntriq X402 Service Homepage](https://x402.ntriq.co.kr) <br>
- [x402 Protocol](https://x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, API Calls, JSON, Guidance] <br>
**Output Format:** [JSON phishing risk assessment with optional agent-facing summary guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a URL or domain input; each service call is disclosed as a paid x402 request.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
