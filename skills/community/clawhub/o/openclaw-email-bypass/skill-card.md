## Description:

Send emails via Google Apps Script when traditional SMTP ports (25/465/587) are blocked.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rishikreddyl](https://clawhub.ai/user/rishikreddyl)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to send plain text or HTML email from environments where outbound SMTP ports are blocked by routing requests through a user-controlled Google Apps Script relay.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Google Apps Script relay is deployed as a public web app, so anyone with the URL and token could attempt to send email through it.

Mitigation: Use a strong rotatable token, restrict deployment access when possible, and add rate limits or access controls before production use.

Risk: Email contents and metadata pass through Google services when the relay sends mail.

Mitigation: Avoid confidential or regulated content unless approved for this data path and review organizational privacy requirements before use.

Risk: The Python helper depends on the unpinned requests package.

Mitigation: Pin dependencies and review updates before installing in managed environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rishikreddyl/skills/openclaw-email-bypass)
- [Setup Guide](references/setup.md)
- [Usage Examples](references/examples.md)
- [Google Apps Script](https://script.google.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown guidance with shell commands and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces commands and helper-code usage for sending email through a configured Google Apps Script relay.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
