## Description: <br>
Complete newsletter management system with subscriber signup (double opt-in), automated welcome drip sequence, broadcast sender, and subscriber analytics. 4 production-ready n8n workflows with Google Sheets backend. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mhmalvi](https://clawhub.ai/user/mhmalvi) <br>

### License/Terms of Use: <br>
CC BY-NC-SA 4.0 <br>


## Use Case: <br>
Developers, operators, content creators, and small businesses use this skill to deploy n8n workflows for subscriber signup, double opt-in confirmation, welcome email drips, broadcast sending, and subscriber analytics with Google Sheets storage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The broadcast workflow can send arbitrary email to all confirmed subscribers. <br>
Mitigation: Review broadcast content and authorization before enabling the workflow, and restrict who can trigger the broadcast webhook. <br>
Risk: The broadcast workflow has a predictable fallback secret if NEWSLETTER_SECRET is missing. <br>
Mitigation: Set a strong NEWSLETTER_SECRET and remove the YOUR_NEWSLETTER_SECRET fallback so broadcasts fail closed when the secret is not configured. <br>
Risk: Subscriber data and outbound email depend on Google Sheets and SMTP credentials. <br>
Mitigation: Use dedicated, low-privilege credentials and verify confirm and unsubscribe handlers before collecting subscribers or enabling scheduled sends. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mhmalvi/newsletter-automation) <br>


## Skill Output: <br>
**Output Type(s):** [configuration, shell commands, guidance] <br>
**Output Format:** [Markdown with JSON workflow files and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires n8n credentials for Google Sheets OAuth2 and SMTP, plus NEWSLETTER_ADMIN_EMAIL, NEWSLETTER_BASE_URL, and NEWSLETTER_SECRET environment variables.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
