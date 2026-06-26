## Description: <br>
Mini-Agent is a MiniMax M2.5-based coding assistant for OpenClaw agents that can read and write files, run shell commands, write code, and manage background processes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[L1-M1ng](https://clawhub.ai/user/L1-M1ng) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to delegate coding, file editing, shell command execution, process management, and configuration tasks to a MiniMax-backed assistant. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad file, shell, and process authority can change project files, overwrite content, or run commands outside the intended task scope. <br>
Mitigation: Use the skill in a sandbox or tightly scoped project directory and manually confirm overwrites, shell commands, and background process actions before relying on the result. <br>
Risk: MiniMax API keys, configuration, and run logs may expose credentials or sensitive task content. <br>
Mitigation: Use a dedicated MiniMax API key, restrict access to ~/.mini-agent/config and ~/.mini-agent/log, and regularly protect, rotate, or delete stored logs and credentials. <br>
Risk: The server security verdict is suspicious because the release grants broad authority without enough scoping or safety guidance. <br>
Mitigation: Review the upstream Mini-Agent source before installing, pin the install source where possible, and scan the release before deployment. <br>


## Reference(s): <br>
- [ClawHub Mini-Agent release](https://clawhub.ai/L1-M1ng/mini-agent) <br>
- [Mini-Agent install source](https://github.com/MiniMax-AI/Mini-Agent.git) <br>
- [MiniMax](https://www.minimaxi.com) <br>
- [MiniMax API platform](https://platform.minimaxi.com) <br>
- [OpenClaw project](https://github.com/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text responses with inline code, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or overwrite files, run foreground or background shell processes, and write logs under ~/.mini-agent/log/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
