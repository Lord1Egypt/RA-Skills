## Description:

macOS desktop-control skill for screenshots, process and system inspection, clipboard access, app and window automation, and optional mouse and keyboard control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asa-zhang](https://clawhub.ai/user/asa-zhang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers on macOS use this skill to let an agent inspect the desktop, capture screenshots, manage apps and processes, use the clipboard, and run local automation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad macOS control permissions can expose screenshots, clipboard contents, application control, and mouse or keyboard actions.

Mitigation: Install only on trusted macOS accounts, grant Accessibility, AppleEvents, and ScreenCapture permissions only when needed, and review proposed commands before execution.

Risk: The security scan reports unsafe persistent command, scheduled task, and sync behavior that needs careful review before installation.

Mitigation: Avoid enabling ClawHub sync or cron helpers until actions are allowlisted, dependencies are pinned, and operation records require explicit review before execution or sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asa-zhang/skills/macos-desktop-control-zhang)
- [macOS permissions guide](references/permissions_guide.md)
- [Troubleshooting guide](references/troubleshooting.md)
- [Basic usage examples](examples/basic_usage.md)
- [AppleScript Language Guide](https://developer.apple.com/library/archive/documentation/AppleScript/Conceptual/AppleScriptLangGuide/)
- [PyAutoGUI documentation](https://pyautogui.readthedocs.io/)
- [macOS privacy and security settings](https://support.apple.com/guide/mac-help/privacy-and-security-mh15209/mac)
- [Vosk model downloads](https://alphacephei.com/vosk/models)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, code, files]

**Output Format:** [Markdown guidance with shell commands, script invocations, and local file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [macOS-only; executed workflows may produce screenshots, operation records, clipboard changes, or desktop automation effects.]

## Skill Version(s):

1.5.3 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
