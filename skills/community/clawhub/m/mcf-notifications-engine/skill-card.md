## Description: <br>
Multi-channel notification delivery with customizable templates, email and SMS sending, and full delivery logging -- built for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cameron48](https://clawhub.ai/user/cameron48) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and AI agent builders use this skill to send email and SMS notifications, manage reusable notification templates, and inspect delivery history through a paid API gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recipient contact details, message contents, delivery history, and payment activity are sent to an external notification gateway. <br>
Mitigation: Install only when the publisher and gateway are trusted, and avoid sensitive personal data until privacy, retention, access control, and billing behavior are documented. <br>
Risk: The skill can send email or SMS messages and incur x402 payment charges. <br>
Mitigation: Require user approval before allowing an agent to send notifications or perform paid API operations. <br>


## Reference(s): <br>
- [Notifications Engine on ClawHub](https://clawhub.ai/cameron48/mcf-notifications-engine) <br>
- [MCF Agentic Gateway](https://gateway.mcfagentic.com) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Configuration, Guidance] <br>
**Output Format:** [Markdown with API endpoint descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses x402 payments in USDC on Base L2 for email, SMS, template, and delivery-log operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
