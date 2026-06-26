## Description: <br>
Automates macOS desktop workflows by capturing screenshots and issuing precise mouse, click, and keyboard commands through local macOS utilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emptyopen](https://clawhub.ai/user/emptyopen) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill when an agent needs to inspect a macOS desktop, locate UI elements, and perform controlled GUI actions. It is suited to local desktop automation tasks where screen contents and input actions can be reviewed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose the full macOS screen to an agent. <br>
Mitigation: Close sensitive windows before use and delete /tmp/claw_view.png after the task is complete. <br>
Risk: The skill can operate the mouse and keyboard on the local desktop. <br>
Mitigation: Require manual approval before actions that submit data, delete content, make purchases, send messages, change settings, or affect accounts. <br>
Risk: The click wrapper depends on a local cliclick binary. <br>
Mitigation: Verify the cliclick binary source and installation path before enabling the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/emptyopen/macos-desktop-control) <br>
- [Skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell command examples and textual tool guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a PNG screenshot at /tmp/claw_view.png when the screen capture wrapper is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
