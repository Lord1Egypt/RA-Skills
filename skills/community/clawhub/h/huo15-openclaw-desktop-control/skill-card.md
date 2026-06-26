## Description: <br>
Guides an agent in using the desktop-control MCP server for macOS automation, emphasizing Accessibility-tree workflows, verified actions, session-state checks, and fallback screenshot-based control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to help an agent operate macOS applications through desktop-control while preferring Accessibility APIs over fragile coordinate clicks. It is intended for tasks such as opening apps, inspecting UI trees, clicking controls, typing, reading screenshots, and recovering from desktop-control errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables broad macOS desktop control through screen, keyboard, mouse, clipboard, and shell-related capabilities. <br>
Mitigation: Install it only in environments where agent desktop control is intended, and limit macOS Accessibility and Screen Recording permissions to those environments. <br>
Risk: Desktop automation may expose private documents, passwords, browser sessions, or account-management workflows to the agent. <br>
Mitigation: Avoid using the skill around sensitive screens and review actions before allowing the agent to interact with private or financial workflows. <br>
Risk: Broad trigger phrases can activate desktop-control behavior for ordinary requests that mention clicking, screenshots, or controlling the computer. <br>
Mitigation: Review the trigger phrases before deployment and require clear user intent before invoking desktop-control tools. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaobod1/huo15-openclaw-desktop-control) <br>
- [Publisher profile](https://clawhub.ai/user/zhaobod1) <br>
- [Homepage](https://cnb.cool/huo15/ai/huo15-skills) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown guidance with command and tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces procedural desktop-automation guidance and example desktop-control MCP tool usage rather than standalone executable code.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, release evidence, _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
