## Description: <br>
Automates macOS GUI tasks by capturing screenshots, reading on-screen text with OCR, controlling mouse and keyboard input, managing windows, and launching apps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DHDragon](https://clawhub.ai/user/DHDragon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent interact with macOS applications through screen reading, mouse and keyboard control, and window automation when direct API or command-line control is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read screen contents and control mouse and keyboard input across macOS applications. <br>
Mitigation: Use it only under supervision, keep sensitive windows and passwords out of view, and revoke Accessibility or Screen Recording permissions when the skill is no longer needed. <br>
Risk: Screenshots used for OCR may capture private information and are written to /tmp/gui-auto by the helper script. <br>
Mitigation: Prefer small region captures and delete /tmp/gui-auto screenshots after use. <br>
Risk: Absolute-coordinate automation can click or type in the wrong place if the screen layout changes. <br>
Mitigation: Confirm the target window and coordinates before executing actions that click, type, submit forms, or change data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DHDragon/macos-gui-automation) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or reference local screenshots under /tmp/gui-auto during agent-guided use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
