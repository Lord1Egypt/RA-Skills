## Description: <br>
Sends emails through the Mailgun API for newsletters, notifications, alerts, and automated reports using configured Mailgun environment variables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manifoldor](https://clawhub.ai/user/manifoldor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent send programmatic email through a configured Mailgun account for alerts, reports, reminders, and similar workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real emails through the configured Mailgun account. <br>
Mitigation: Install and use it only for approved Mailgun sending workflows, and review message content and recipients before sending. <br>
Risk: Mailgun API keys and email content may expose sensitive information if handled carelessly. <br>
Mitigation: Protect the API key, prefer narrowly scoped credentials when available, and avoid sending secrets or regulated data unless Mailgun is approved for that data. <br>


## Reference(s): <br>
- [Mailgun API Reference](references/api.md) <br>
- [Mailgun Documentation](https://documentation.mailgun.com/) <br>
- [OpenClaw repository](https://github.com/openclaw/openclaw) <br>
- [ClawHub skill page](https://clawhub.ai/manifoldor/mailgun) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, Text] <br>
**Output Format:** [Markdown guidance with shell command examples and command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Mailgun environment variables for API key, domain, sender, and default recipient.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
