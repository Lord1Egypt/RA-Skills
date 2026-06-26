## Description: <br>
macOS 桌面微信自动发送文件/消息。AppleScript + cliclick 驱动，无需浏览器。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[myljs](https://clawhub.ai/user/myljs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and desktop automation users on macOS use this skill to send WeChat messages or files from an already logged-in WeChat desktop session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically send real WeChat messages or files from the user's logged-in desktop account. <br>
Mitigation: Review contacts, message text, and file paths before execution, and use it only when automated sending from the logged-in account is intended. <br>
Risk: Desktop automation, clipboard use, and fixed screen coordinates may send content to the wrong recipient or active window. <br>
Mitigation: Keep WeChat visible and positioned as expected, verify the selected chat before sending, and avoid using the skill for sensitive files unless that delivery risk is accepted. <br>
Risk: Untrusted message text or file paths can affect automated input behavior. <br>
Mitigation: Avoid passing untrusted text into the tool and verify file paths before invoking the sender. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/myljs/mac-wechat-sender) <br>
- [Publisher profile](https://clawhub.ai/user/myljs) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces command-line usage guidance for sending WeChat messages or files through macOS desktop automation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
