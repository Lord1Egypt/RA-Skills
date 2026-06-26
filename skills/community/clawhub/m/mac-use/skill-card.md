## Description: <br>
Control macOS GUI apps visually — take screenshots, click, scroll, type. Use when the user asks to interact with any Mac desktop application's graphical interface. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kekejun](https://clawhub.ai/user/kekejun) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to let an agent inspect and control macOS desktop applications through a screenshot, OCR, action, and verification loop. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can capture the Mac screen and control mouse and keyboard input. <br>
Mitigation: Install it only when broad local GUI control is intended, avoid sensitive screens, and require explicit human approval before actions that send, buy, delete, approve, or change account or security settings. <br>
Risk: Screenshots and OCR element maps are written to temporary files. <br>
Mitigation: Delete /tmp/mac_use*.png and /tmp/mac_use_elements.json after use, especially after interacting with private applications. <br>
Risk: The type command uses clipboard paste and can expose or overwrite clipboard contents. <br>
Mitigation: Do not type passwords or secrets through the skill, and clear or restore the clipboard after use when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kekejun/mac-use) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and JSON command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces annotated screenshot paths and element JSON from local macOS GUI interactions.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
