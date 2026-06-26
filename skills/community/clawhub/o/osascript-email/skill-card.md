## Description: <br>
Send plain-text email from macOS through Mail.app using AppleScript without SMTP credentials, passwords, or API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yumik20](https://clawhub.ai/user/yumik20) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to send plain-text status reports, standup updates, alerts, and cron-generated messages from a configured macOS Mail.app account when SMTP or other mail tools are unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send email silently through Mail.app. <br>
Mitigation: Require explicit user approval before each send and confirm the configured sender account, recipients, subject, body, and attachments. <br>
Risk: The helper builds executable AppleScript from input values with insufficient validation. <br>
Mitigation: Do not pass untrusted or externally supplied recipient, sender, subject, body, or file path values until AppleScript escaping and validation are fixed. <br>
Risk: Attachment examples can send local files when given an absolute path. <br>
Mitigation: Use only approved absolute file paths, verify the file exists, and avoid large or sensitive attachments. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/yumik20/osascript-email) <br>
- [Sending Attachments via osascript-email](references/attachments.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with AppleScript, bash, and Python code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces commands and helper code for plain-text Mail.app sends; attachment examples are optional and require absolute file paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
