## Description: <br>
Helps an agent inspect and control macOS system functions, including system status, process management, audio and brightness, networking, power actions, screenshots, clipboard access, Finder actions, and System Settings shortcuts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlutwuwei](https://clawhub.ai/user/dlutwuwei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical operators, and macOS users use this skill when they want an agent to help inspect local system state or propose common macOS command-line actions. It is intended for local system-control workflows such as checking resources, managing processes, changing settings, taking screenshots, or opening Finder and System Settings targets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local system commands can terminate processes, shut down or restart the machine, toggle Wi-Fi, empty Trash, or change Finder preferences. <br>
Mitigation: Require explicit user confirmation for destructive or disruptive actions and show the exact command target before execution. <br>
Risk: Screenshots and clipboard reads can expose sensitive local information. <br>
Mitigation: Treat screenshot files and clipboard contents as sensitive and confirm intent before capturing, reading, or sharing them. <br>
Risk: Some commands may require sudo access, macOS privacy permissions, or optional utilities such as brightness. <br>
Mitigation: Tell the user when elevated privileges, system permissions, or extra command-line tools are required before attempting the action. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that require user confirmation, sudo access, macOS permissions, or local command-line utilities.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
