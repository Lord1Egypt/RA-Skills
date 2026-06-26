## Description: <br>
Helps users set up and run MobiZen-GUI to automate Android phone operations via natural language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xjx0524](https://clawhub.ai/user/xjx0524) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and mobile automation practitioners use this skill to install and configure MobiZen-GUI, connect Android devices through ADB, select an OpenAI-compatible or local model endpoint, and run natural-language mobile tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide real Android device automation, which may perform unintended actions or affect sensitive apps. <br>
Mitigation: Use a test device or non-sensitive profile first, supervise runs directly, and avoid financial, account, or messaging tasks unless each action is reviewed. <br>
Risk: Screenshots, prompts, API keys, wireless ADB sessions, and local model servers can expose sensitive data or device access. <br>
Mitigation: Prefer trusted or local model endpoints for sensitive screens, protect API keys, keep ADB over USB where possible, and clean up screenshots, ADBKeyboard, wireless ADB, and model servers after use. <br>


## Reference(s): <br>
- [MobiZen-GUI repository](https://github.com/alibaba/MobiZen-GUI) <br>
- [Android SDK Platform Tools](https://developer.android.com/studio/releases/platform-tools) <br>
- [ADBKeyboard repository](https://github.com/senzhk/ADBKeyBoard) <br>
- [MobiZen-GUI-4B model](https://modelscope.cn/models/GUIAgent/MobiZen-GUI-4B) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown with bash, YAML, and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask for model endpoint settings and produce configuration guidance or commands that affect a connected Android device.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
