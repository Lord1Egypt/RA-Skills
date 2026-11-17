## Description:

手机操控技能。通过 USB ADB 连接安卓手机，捕获屏幕、分析 UI 元素、执行点击、滑动、输入等操作。当用户要求操控手机、执行 App 操作、打开应用、发送消息时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanlan314](https://clawhub.ai/user/lanlan314)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to control an owned USB-connected Android phone through ADB, including inspecting UI dumps, tapping or swiping, entering ASCII text, launching apps, and handling simple app workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can issue broad ADB controls against a real Android device, including taps, swipes, text entry, app launch, and force-stop operations.

Mitigation: Use only with an owned device where broad ADB control is acceptable, and require explicit confirmation before sensitive actions such as sending messages or force-stopping apps.

Risk: Screenshots and UI dumps can contain sensitive screen contents and may remain in temporary files or /sdcard/dump.xml.

Mitigation: Avoid running the skill on sensitive screens and delete generated screenshots, UI dump files, and /sdcard/dump.xml after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lanlan314/skills/phone-agent-lan)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples, plus text command output and generated screenshot or UI dump file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create temporary screenshot PNG files, temporary UI XML dumps, and /sdcard/dump.xml on the connected Android device.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
