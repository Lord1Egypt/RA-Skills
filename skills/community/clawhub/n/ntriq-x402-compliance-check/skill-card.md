## Description: <br>
AI compliance analysis for contracts, policies, and text. Detects issues and recommends fixes. $0.03 USDC via x402. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ntriq-gh](https://clawhub.ai/user/ntriq-gh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, legal operations teams, and compliance reviewers use this skill to submit contracts, policies, or other text to an external x402 API for GDPR, HIPAA, SOX, corporate policy, or custom-framework analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected text to an external API at x402.ntriq.co.kr for analysis. <br>
Mitigation: Confirm the provider is trusted and avoid submitting confidential client data, regulated health data, or sensitive business records unless authorized. <br>
Risk: Each compliance check authorizes a $0.03 USDC payment using the x402 protocol on Base mainnet. <br>
Mitigation: Review payment authorization details before use and only send requests when the fee and network are acceptable. <br>
Risk: Compliance analysis may be incomplete or unsuitable as final legal advice. <br>
Mitigation: Use returned violations and recommendations as review input and have qualified reviewers validate decisions for the relevant framework and jurisdiction. <br>


## Reference(s): <br>
- [Ntriq x402 compliance service](https://x402.ntriq.co.kr) <br>
- [x402 protocol](https://x402.org) <br>
- [ClawHub skill page](https://clawhub.ai/ntriq-gh/ntriq-x402-compliance-check) <br>
- [Publisher profile](https://clawhub.ai/user/ntriq-gh) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, guidance, API calls, shell commands] <br>
**Output Format:** [Markdown guidance with JSON API examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns compliance status, risk level, issues, severity, recommendations, and summary from a paid external API.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
