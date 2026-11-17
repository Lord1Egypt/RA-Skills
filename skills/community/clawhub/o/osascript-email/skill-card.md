## Description:

Send plain-text emails on macOS through Mail.app using AppleScript without SMTP credentials, passwords, or API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yumik20](https://clawhub.ai/user/yumik20)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to send standup reports, alerts, and other trusted plain-text email from a configured macOS Mail.app account when SMTP or other mail tools are unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can silently send email from a configured macOS Mail.app account.

Mitigation: Use only with explicit user consent and restrict recipient, sender, subject, body, and attachment values to trusted inputs.

Risk: Helper code builds executable AppleScript from email fields and attachment paths with insufficient validation.

Mitigation: Validate addresses and absolute attachment paths, pass values as data where possible, and require review before sending or attaching files.

## Reference(s):

- [Sending Attachments via osascript-email](references/attachments.md)
- [ClawHub skill page](https://clawhub.ai/yumik20/skills/osascript-email)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with bash, AppleScript, and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs guidance and helper code for Mail.app email sending; the helper prints send status or raises an error on osascript failure.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
