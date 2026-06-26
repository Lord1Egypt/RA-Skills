## Description: <br>
Control the Niri Wayland compositor on Linux via its IPC (`niri msg --json` / $NIRI_SOCKET) to query compositor state or perform desktop actions from an OpenClaw agent running inside a Niri session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AtefR](https://clawhub.ai/user/AtefR) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and desktop automation users use this skill to inspect Niri outputs, workspaces, windows, focused state, and event streams, then issue compositor actions such as focusing, moving, or closing windows. It is intended for agents operating in a Linux Niri desktop session with explicit access to the compositor IPC interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes broad desktop IPC authority, including actions that can close windows, reload compositor configuration, or affect monitor and workspace state. <br>
Mitigation: Require explicit user approval before state-changing compositor actions and prefer read-only queries when gathering context. <br>
Risk: Raw IPC and spawn-sh access can execute powerful operations inside the active desktop session. <br>
Mitigation: Avoid unattended automation, review raw IPC payloads before sending them, and require approval before spawning commands. <br>


## Reference(s): <br>
- [Niri IPC quick reference](references/ipc.md) <br>
- [Upstream niri-ipc crate documentation](https://yalter.github.io/niri/niri_ipc/) <br>
- [ClawHub skill page](https://clawhub.ai/AtefR/niri-ipc) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, text] <br>
**Output Format:** [Markdown with inline shell commands, Python helper invocations, and JSON IPC examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include normalized JSON from Niri IPC queries or event streams.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
