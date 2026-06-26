## Description: <br>
Control mouse and keyboard on Mac using cliclick. Use when you need to automate clicking, typing, or controlling the mouse cursor. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[calvin-dean](https://clawhub.ai/user/calvin-dean) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to automate mouse movement, clicking, typing, and keyboard actions on macOS with cliclick during browser or application workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent-driven UI automation can click or type into unintended applications or authenticated sessions. <br>
Mitigation: Use isolated test accounts and temporary sessions, verify the target window and coordinates before execution, and avoid personal or production profiles unless explicitly intended. <br>
Risk: Security evidence flags high-impact browser control, session storage access, and unsafe raw code execution paths. <br>
Mitigation: Install only for intended browser testing or debugging, review scripts before execution, and do not save or commit auth-state files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/calvin-dean/mouse-keyboard) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands target macOS UI automation through cliclick.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
