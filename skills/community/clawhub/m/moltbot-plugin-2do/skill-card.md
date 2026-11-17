## Description:

Creates tasks from Chinese or English natural language, extracts task title, due date or time, priority, list, and tags, then sends a formatted email to the user's configured 2Do inbox.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chuckiefan](https://clawhub.ai/user/chuckiefan)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to turn natural-language reminders, todos, and task requests into 2Do tasks through an SMTP mailbox configured for Email to 2Do capture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad task triggers can send raw user messages through SMTP without a clear confirmation step.

Mitigation: Narrow activation to explicit task commands or add a preview and confirmation step before sending email.

Risk: The skill requires SMTP credentials and a configured 2Do inbox address.

Mitigation: Use an app-specific SMTP password, store credentials as environment secrets, and prefer a dedicated mailbox where possible.

Risk: If the built dist/main.js file is missing, execution can fall back to npx-based TypeScript execution.

Mitigation: Build the package before deployment so dist/main.js exists and avoid the npx fallback in production.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chuckiefan/moltbot-plugin-2do)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [2Do](https://www.2doapp.com)
- [2Do Email to 2Do knowledge base](https://www.2doapp.com/kb/category/ios/email-to-2do/44/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and plain-text execution status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and SMTP/2Do environment variables; sends email as a side effect.]

## Skill Version(s):

1.0.2 (source: package.json, CHANGELOG, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
