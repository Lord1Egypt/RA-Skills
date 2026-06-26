## Description: <br>
Menu bar context monitor for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hjklasdfg](https://clawhub.ai/user/hjklasdfg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install and operate a macOS SwiftBar menu bar monitor that shows recent agent activity, model aliases, status, and context-token usage for local or SSH-accessible OpenClaw hosts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs a persistent SwiftBar plugin that can keep polling an OpenClaw host over SSH. <br>
Mitigation: Install it only when persistent menu bar monitoring is intended, and remove or disable the SwiftBar plugin when polling should stop. <br>
Risk: Remote mode copies and runs the status collector on an SSH-accessible host. <br>
Mitigation: Use remote mode only with a host you control, review the installer before running it, and rely on SSH key authentication. <br>
Risk: The SwiftBar plugin can use OPENCLAW_STATUS_SCRIPT to choose the remote status command. <br>
Mitigation: Do not set OPENCLAW_STATUS_SCRIPT unless the command is fully trusted. <br>


## Reference(s): <br>
- [Context Monitor on ClawHub](https://clawhub.ai/hjklasdfg/menubar-context-monitor) <br>
- [SwiftBar](https://github.com/swiftbar/SwiftBar) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May install local files and configure a recurring SwiftBar plugin that polls a local or SSH-accessible OpenClaw host.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata; artifact SKILL.md lists 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
