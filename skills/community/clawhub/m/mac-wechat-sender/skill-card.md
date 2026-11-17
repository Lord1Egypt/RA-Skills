## Description:

macOS 桌面微信自动发送文件/消息。AppleScript + cliclick 驱动，无需浏览器。

This skill is ready for commercial/non-commercial use.

## Publisher:

[myljs](https://clawhub.ai/user/myljs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and desktop automation users use this skill to send WeChat messages or local files from a macOS desktop session through AppleScript and cliclick.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can immediately send real WeChat messages or local files.

Mitigation: Use only trusted, manually reviewed contact names, message text, and file paths; add an explicit confirmation step before sending.

Risk: Crafted input can trigger AppleScript injection when contact names, messages, or file paths are interpolated into scripts.

Mitigation: Pass user-controlled values through argv-based AppleScript handling or another structured escaping approach before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/myljs/skills/mac-wechat-sender)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Guidance]

**Output Format:** [Markdown with inline shell commands and plain-text status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS, a logged-in WeChat desktop app, and cliclick.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
