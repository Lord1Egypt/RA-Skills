## Description: <br>
Bi-directional control of Trae via macOS AppleScript with built-in feedback mechanism. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[88901111hz-lang](https://clawhub.ai/user/88901111hz-lang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to send instructions to Trae on macOS, wait for a file-based completion signal, and collect feedback from the automated workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad UI-driven ability to send code or command instructions into Trae. <br>
Mitigation: Use it only with trusted prompts and trusted projects, keep the Trae window visible while it runs, and review requested actions before relying on the result. <br>
Risk: Instructions are passed through the macOS clipboard, which can expose sensitive prompt content. <br>
Mitigation: Avoid including secrets, credentials, or confidential data in instructions sent through this skill. <br>
Risk: The workflow depends on macOS Accessibility automation and the currently focused application. <br>
Mitigation: Grant Accessibility permissions only when intentionally using the skill and confirm Trae is the focused target before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/88901111hz-lang/nerve-bridge-skill) <br>
- [Publisher profile](https://clawhub.ai/user/88901111hz-lang) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, code, text] <br>
**Output Format:** [Markdown with inline shell and Python examples; runtime feedback is JSON text when the Trae signal file is received.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS, python3, osascript, an active Trae window, and Accessibility permissions for UI automation.] <br>

## Skill Version(s): <br>
v1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
