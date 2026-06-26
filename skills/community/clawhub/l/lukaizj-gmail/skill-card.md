## Description: <br>
Gmail integration - Send emails, manage labels, and automate Gmail workflows with full OAuth2 support <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lukaizj](https://clawhub.ai/user/lukaizj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent send Gmail messages, list recent inbox messages, and create labels after configuring Google OAuth client credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive Google OAuth credentials for an email account. <br>
Mitigation: Use a dedicated, least-privilege Google OAuth client and keep the client secret out of code, prompts, and shared logs. <br>
Risk: The skill can send email and change labels, which may affect real mailbox content. <br>
Mitigation: Require explicit human review before sending messages or changing labels, especially on production or personal accounts. <br>
Risk: Authentication and action boundaries are under-specified in the security evidence. <br>
Mitigation: Verify the OAuth flow and granted scopes before connecting a real Gmail account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lukaizj/lukaizj-gmail) <br>
- [Publisher profile](https://clawhub.ai/user/lukaizj) <br>
- [Project homepage](https://github.com/lukaizj/gmail-integration-skill) <br>
- [Google Cloud Console](https://console.cloud.google.com/) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, Configuration] <br>
**Output Format:** [JSON-like tool responses and agent-visible text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GMAIL_CLIENT_ID and GMAIL_CLIENT_SECRET environment variables for Google OAuth configuration.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and claw.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
