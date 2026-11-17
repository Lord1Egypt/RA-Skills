## Description:

Controls rooted Android devices through OpenClaw by running shell commands for app management, touch and key input, text entry, file listing, and screenshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssrlxl123](https://clawhub.ai/user/ssrlxl123)

### License/Terms of Use:


## Use Case:

Developers, QA engineers, and device operators use this skill to automate Android app testing, remote device control, installed-app management, screenshots, and repeatable device operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Root-level Android control can clear app data, install or uninstall packages, capture screenshots, list files, and send input to apps.

Mitigation: Use only on devices where root-level remote control is intended, and require explicit confirmation for clear, install, uninstall, screenshot, ls, and text actions.

Risk: Text commands and execution logs may expose passwords, tokens, paths, package names, or sensitive screen content.

Mitigation: Avoid entering secrets through text input, review logs created under device storage, and remove troubleshooting logs when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ssrlxl123/skills/openclaw-android)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Code]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target a rooted Android device and may write execution logs on device storage.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
