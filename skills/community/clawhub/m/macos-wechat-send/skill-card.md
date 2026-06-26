## Description: <br>
Automates WeChat for macOS to send text messages and local files to selected contacts using AppleScript and clipboard-based paste actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sincerememe](https://clawhub.ai/user/sincerememe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and macOS automation users use this skill to send approved WeChat messages and attachments from an agent workflow. It is useful for local personal automation where the recipient, text, and file paths are explicitly supplied by the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can immediately send real WeChat messages and files from the user's account. <br>
Mitigation: Run it only for explicit user-approved recipients, message text, and file paths, and review command arguments before execution. <br>
Risk: Clipboard and Finder automation may expose or send unintended local content, especially when sensitive attachments are involved. <br>
Mitigation: Avoid sensitive attachments, verify each file path before sending, and restore or review clipboard contents after use. <br>
Risk: The shell wrapper falls back to an unbundled hard-coded virtual environment path. <br>
Mitigation: Install and run the skill from a trusted local environment, and confirm the virtual environment path before granting automation permissions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sincerememe/macos-wechat-send) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Python automation script](artifact/wechat-send.py) <br>
- [Shell wrapper](artifact/wechat-send.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text command output and Markdown usage guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS, WeChat for Mac logged in, Python 3, a suitable Python virtual environment, and macOS Accessibility permissions; uses the clipboard and Finder automation for message and file sending.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
