## Description:

PhishGuard monitors Gmail and Outlook inboxes for phishing, analyzes incoming email with static rules and Claude API analysis, assigns a risk score, and can label suspicious messages or send Slack and Teams alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lichq1337](https://clawhub.ai/user/lichq1337)

### License/Terms of Use:

MIT-0

## Use Case:

Security teams and administrators use this skill to monitor business email for phishing indicators, receive scored analysis reports, and apply warning or quarantine labels to suspicious Gmail messages. It is designed for organizations of about 20 to 200 users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill continuously reads business email and sends selected email fields to Anthropic and optional Slack or Teams alert channels.

Mitigation: Use a dedicated monitored mailbox or tightly scoped Google account, protect local environment files, and confirm which email fields may be shared with each third-party service before deployment.

Risk: The skill can automatically apply Gmail warning and quarantine labels to messages based on risk scoring.

Mitigation: Disable or constrain automatic labeling during review, test on non-production mailboxes, and require administrator approval before broad mailbox deployment.

Risk: The security evidence flags unsafe shell-command handling, and the installation guide includes a curl-to-bash installer path.

Mitigation: Avoid the curl-to-bash path, prefer reviewed package installation steps, and fix command construction and input scoping before enabling the Gmail adapter in production.

## Reference(s):

- [ClawHub PhishGuard Skill Page](https://clawhub.ai/lichq1337/skills/phishguard)
- [PhishGuard Installation Guide](artifact/INSTALACION.md)
- [PhishGuard Skill Definition](artifact/SKILL.md)
- [Anthropic Messages API Endpoint](https://api.anthropic.com/v1/messages)
- [Slack Apps Configuration](https://api.slack.com/apps)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with inline shell and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces risk level, numeric score, detected indicators, AI summary, recommended action, session report text, Gmail labels, and optional Slack or Teams alert messages.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
