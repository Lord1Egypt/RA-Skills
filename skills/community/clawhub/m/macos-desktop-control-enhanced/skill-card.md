## Description: <br>
macOS Desktop Control Enhanced provides system-wide desktop automation on macOS, including screenshot capture, process management, clipboard operations, system information, application control, and direct mouse, keyboard, and screen interaction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pry520okgpt](https://clawhub.ai/user/pry520okgpt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to let an agent query or control a macOS desktop, including screenshots, clipboard actions, application focus, process management, mouse input, and keyboard input. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can capture screen contents, read or write clipboard data, type text, click, focus apps, and terminate processes, which can expose sensitive data or disrupt active work. <br>
Mitigation: Require explicit user approval before desktop-control actions, avoid use around passwords, private messages, terminals, admin prompts, and unsaved work, and review proposed coordinates, text, app identifiers, and process targets before execution. <br>
Risk: The skill's broad macOS automation surface can perform unintended actions if inputs are wrong or generated without enough context. <br>
Mitigation: Prefer narrow, task-specific commands, confirm destructive actions such as process termination, and run in a controlled desktop session when possible. <br>


## Reference(s): <br>
- [macOS Desktop Control Enhanced API Reference](references/api_reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/pry520okgpt/macos-desktop-control-enhanced) <br>
- [Publisher profile](https://clawhub.ai/user/pry520okgpt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown, Python code, shell commands, and plain-text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or modify local desktop state through screenshots, clipboard updates, app control, mouse actions, keyboard actions, and process termination.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
