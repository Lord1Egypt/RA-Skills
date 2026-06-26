## Description: <br>
macOS desktop control via native tools for screenshots, process management, system information, clipboard operations, and app control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asa-zhang](https://clawhub.ai/user/asa-zhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users use this skill to inspect and automate a local macOS desktop through shell scripts, AppleScript, and optional Python mouse and keyboard control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad macOS automation permissions, including Accessibility, AppleEvents, and ScreenCapture. <br>
Mitigation: Install only in trusted macOS environments and grant permissions only to the terminal or agent host that must run the automation. <br>
Risk: The security scan reports under-disclosed cloud sync, cron scheduling, and raw command execution paths. <br>
Mitigation: Avoid enabling CLAWHUB_API_KEY, setup_cron.sh, scheduled_task.sh, or ControlMemory sync unless scheduled execution and operation-history sharing are intentional. <br>
Risk: Natural-language, clipboard, QQ, and stored-script paths may execute or reuse sensitive or untrusted input. <br>
Mitigation: Review controlmemory.md and avoid passing untrusted text into command, clipboard, messaging, or stored-operation workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/asa-zhang/macos-desktop-control-zhang) <br>
- [permissions_guide.md](references/permissions_guide.md) <br>
- [troubleshooting.md](references/troubleshooting.md) <br>
- [basic_usage.md](examples/basic_usage.md) <br>
- [AppleScript Language Guide](https://developer.apple.com/library/archive/documentation/AppleScript/Conceptual/AppleScriptLangGuide/) <br>
- [PyAutoGUI documentation](https://pyautogui.readthedocs.io/) <br>
- [Vosk models](https://alphacephei.com/vosk/models) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell and Python commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local desktop automation instructions and command invocations for macOS; some actions require macOS privacy permissions or optional Python dependencies.] <br>

## Skill Version(s): <br>
1.5.3 (source: frontmatter, package.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
