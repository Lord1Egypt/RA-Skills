## Description:

Send outbound emails via the Mailgun API. Uses MAILGUN_API_KEY, MAILGUN_DOMAIN, MAILGUN_REGION, and MAILGUN_FROM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lksrz](https://clawhub.ai/user/lksrz)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to let an agent send outbound email through a configured Mailgun account and verified sending domain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires access to a Mailgun API key.

Mitigation: Use a scoped Mailgun key where possible, store it only in the runtime environment, and rotate it if exposure is suspected.

Risk: Email recipients, subjects, and bodies are sent to Mailgun.

Mitigation: Do not use the skill for secrets or regulated data unless the Mailgun account and workflow are approved for that data.

Risk: The skill can send outbound email from the configured domain.

Mitigation: Restrict use to approved sending domains and review generated recipient, subject, and body content before sending.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lksrz/skills/mailgun-simple)
- [ClawHub publisher profile](https://clawhub.ai/user/lksrz)
- [Mailgun API security settings](https://app.mailgun.com/settings/api_security)
- [Mailgun EU API endpoint](https://api.eu.mailgun.net)
- [Mailgun US API endpoint](https://api.mailgun.net)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Text, Guidance]

**Output Format:** [CLI command invocation and Mailgun API response or status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and the MAILGUN_API_KEY, MAILGUN_DOMAIN, MAILGUN_REGION, and MAILGUN_FROM environment variables.]

## Skill Version(s):

2.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
