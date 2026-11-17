## Description:

Automates sending WeChat for Mac text messages and files to specified contacts by controlling the macOS UI with AppleScript and clipboard operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sincerememe](https://clawhub.ai/user/sincerememe)

### License/Terms of Use:

MIT-0

## Use Case:

Mac users and automation agents use this skill to send ordered batches of WeChat text messages and local files from a logged-in WeChat for Mac session. It is intended for user-directed messaging where the recipient and content are known before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send real WeChat messages and files without a separate confirmation boundary.

Mitigation: Confirm the recipient, message text, and file list before execution, and run it only from the intended logged-in WeChat account.

Risk: The skill controls the macOS UI and overwrites clipboard contents during operation.

Mitigation: Grant accessibility permissions only in trusted sessions, avoid concurrent sensitive clipboard workflows, and expect clipboard contents to be replaced.

Risk: The security guidance identifies unusual or untrusted file paths as risky until AppleScript path handling and recipient verification are fixed.

Mitigation: Use normal trusted absolute file paths, avoid sensitive files, and manually verify the chat window before sending files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sincerememe/skills/macos-wechat-send)
- [Publisher profile](https://clawhub.ai/user/sincerememe)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with shell command examples and plain-text execution guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces user-facing instructions and command invocations for macOS WeChat automation; runtime actions may send messages or files from the active WeChat account.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
