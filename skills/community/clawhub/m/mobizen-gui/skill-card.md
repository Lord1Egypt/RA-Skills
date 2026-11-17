## Description:

Helps users set up and run MobiZen-GUI to automate Android phone operations from natural-language instructions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xjx0524](https://clawhub.ai/user/xjx0524)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install and configure MobiZen-GUI, connect Android devices through ADB, configure model endpoints, and customize automation components for mobile-use tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential exposure through model API configuration or chat-provided secrets.

Mitigation: Do not paste production API keys into chat, keep secrets out of project files, and use restricted or disposable credentials for setup.

Risk: Android device control through ADB can perform unintended phone input actions.

Mitigation: Prefer USB ADB, avoid network ADB, test on non-production devices, and review commands before running automation.

Risk: Remote code, APKs, models, and dependencies may be unpinned or untrusted.

Mitigation: Verify APK, model, and dependency sources before installation and run the model stack in a restricted environment.

Risk: Local model services can expose network endpoints if bound broadly.

Mitigation: Bind local model servers to 127.0.0.1 unless a reviewed deployment requires broader network access.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xjx0524/skills/mobizen-gui)
- [MobiZen-GUI Repository](https://github.com/alibaba/MobiZen-GUI)
- [ADBKeyboard Repository](https://github.com/senzhk/ADBKeyBoard)
- [Android SDK Platform Tools](https://developer.android.com/studio/releases/platform-tools)
- [MobiZen-GUI-4B ModelScope Model](https://modelscope.cn/models/GUIAgent/MobiZen-GUI-4B)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash, YAML, and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include setup commands, configuration values, and code customization examples.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
