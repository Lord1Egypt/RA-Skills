## Description: <br>
Send outbound emails via the Mailgun API. Uses MAILGUN_API_KEY, MAILGUN_DOMAIN, MAILGUN_REGION, and MAILGUN_FROM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lksrz](https://clawhub.ai/user/lksrz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation agents use this skill to send transactional or operational emails through a configured Mailgun account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send outbound email through the configured Mailgun account. <br>
Mitigation: Review the recipient, subject, body, sender, sending domain, and region before execution. <br>
Risk: The skill requires a private Mailgun API key in the environment. <br>
Mitigation: Use the narrowest practical Mailgun key, keep it out of source control and logs, and rotate it if exposure is suspected. <br>
Risk: Email bodies may contain sensitive, regulated, or secret information. <br>
Mitigation: Avoid sending secrets or regulated data unless Mailgun handling is approved for the intended use case. <br>


## Reference(s): <br>
- [Mailgun Simple release page](https://clawhub.ai/lksrz/mailgun-simple) <br>
- [lksrz publisher profile](https://clawhub.ai/user/lksrz) <br>
- [Mailgun API security settings](https://app.mailgun.com/settings/api_security) <br>
- [Mailgun EU API endpoint](https://api.eu.mailgun.net) <br>
- [Mailgun US API endpoint](https://api.mailgun.net) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, text] <br>
**Output Format:** [Plain text command output from a Node.js helper and Mailgun API response messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sending email requires Mailgun credentials, a verified sending domain, and the selected Mailgun region.] <br>

## Skill Version(s): <br>
2.2.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
