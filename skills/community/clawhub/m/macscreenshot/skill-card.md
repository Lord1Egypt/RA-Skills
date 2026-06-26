## Description: <br>
Capture macOS screenshots for the whole screen, a specific app window, or a precisely targeted desktop window using built-in system tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mallocfeng](https://clawhub.ai/user/mallocfeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, employees, and external users can use this skill to capture full-screen or targeted macOS window screenshots while keeping the screenshot as a local file unless the user explicitly asks to share it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Screenshots can capture confidential or private on-screen information. <br>
Mitigation: Save screenshots locally by default, review the saved file before sharing, and only attach or send the PNG when the user explicitly requests delivery. <br>
Risk: macOS screen recording permission grants the agent host process visibility into screen content. <br>
Mitigation: Install only when that access is acceptable and enable Screen Recording only for the actual host process needed to run the skill. <br>
Risk: Targeted window capture can fail when the selected window is not shareable or is not visible on screen. <br>
Mitigation: Confirm the window is on screen and shareable, prefer entries with sharing state 1, and ask the user to bring the target window forward before retrying. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mallocfeng/macscreenshot) <br>
- [Publisher profile](https://clawhub.ai/user/mallocfeng) <br>
- [Success notes](references/success-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and local PNG file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a local screenshot path by default and only sends or attaches the PNG when explicitly requested.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
