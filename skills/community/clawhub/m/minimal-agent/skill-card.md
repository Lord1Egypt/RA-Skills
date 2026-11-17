## Description:

Minimal Agent helps an agent control a Windows desktop through system-controller for window, process, hardware, GUI automation, serial, and IoT tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent automate Windows desktop control, process and hardware actions, GUI/OCR workflows, serial communication, and IoT interactions. It supports structured controller-tool execution as well as text and mixed modes that can run shell commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text and mixed modes can execute arbitrary shell commands and change local system state.

Mitigation: Prefer function-only mode for normal use, and avoid text or mixed mode on machines with sensitive files, credentials, business data, or production access.

Risk: Auto mode can fall back to unrestricted command execution when the external system-controller dependency is unavailable.

Mitigation: Pin and verify the system-controller dependency before use, and configure function or force_function mode when fallback execution is not acceptable.

Risk: Weak confirmation controls may not cover every destructive or state-changing action.

Mitigation: Review requested actions before execution and require operator approval for process, power, network, file, and shell-command changes.

## Reference(s):

- [Minimal Agent ClawHub release](https://clawhub.ai/wangjiaocheng/skills/minimal-agent)
- [system-controller dependency on ClawHub](https://clawhub.ai/wangjiaocheng/system-controller)
- [system-controller dependency on Tencent SkillHub](https://skillhub.tencent.com/skills/system-controller)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text, command output, and concise execution results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May change OS, hardware, GUI, network, serial, and IoT state depending on the selected mode.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
