## Description:

AI-powered email triage via IMAP (himalaya) or Google API. Fetches inbox, classifies messages by urgency, recommends actions, and generates daily markdown digests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gruted](https://clawhub.ai/user/gruted)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to fetch recent inbox and calendar data, classify email urgency and category, recommend actions, and produce daily triage digests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox and calendar access can expose sensitive personal or business information.

Mitigation: Install only when the configured backend's inbox and calendar access is acceptable for the intended environment.

Risk: OAuth credentials, Gmail app passwords, and API keys can grant ongoing account or model-provider access if mishandled.

Mitigation: Keep credentials scoped and private, and review local environment files before use.

Risk: Optional AI classification may send message content through the configured AI data flow.

Mitigation: Disable optional AI classification unless that data flow is acceptable for the emails being triaged.

Risk: Cron configuration can run unattended triage and append recurring local digest files.

Mitigation: Add the cron job only when recurring unattended execution and local digest retention are intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gruted/skills/gruted-inbox-triage)
- [GitHub project](https://github.com/gruted/inbox-triage-bot)
- [Project landing page](https://gruted.github.io/inbox-triage-bot/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON-producing command descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate recurring local markdown digest files when configured through cron.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
