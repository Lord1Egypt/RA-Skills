## Description:

Control the Niri Wayland compositor on Linux via its IPC (`niri msg --json` / `$NIRI_SOCKET`) to query compositor state and perform actions such as focusing, moving, or closing windows, switching workspaces, spawning commands, and reloading configuration from an OpenClaw agent running in a Niri session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atefr](https://clawhub.ai/user/atefr)

### License/Terms of Use:


## Use Case:

Developers and desktop automation users use this skill to let an agent inspect and control a local Niri Wayland compositor session. It supports querying outputs, workspaces, windows, and focused state, then issuing compositor actions through `niri msg --json` or direct `$NIRI_SOCKET` IPC.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad control of the active Niri desktop session, including focus changes, window movement, close-window actions, output changes, and config reloads.

Mitigation: Review planned compositor actions before execution, prefer read-only queries first, and use exact window IDs or precise workspace names for actions that change or close windows.

Risk: Raw IPC and `spawn-sh` can execute high-impact requests or shell commands in the user's desktop session.

Mitigation: Avoid raw IPC and shell-spawn paths unless necessary; inspect command arguments and JSON requests before running them.

Risk: Substring-based window matching can affect the wrong window when titles or app IDs overlap.

Mitigation: List matching windows first, refine the query, and prefer exact IDs for destructive operations.

## Reference(s):

- [Niri IPC quick reference](references/ipc.md)
- [Upstream niri-ipc crate docs](https://yalter.github.io/niri/niri_ipc/)
- [ClawHub skill page](https://clawhub.ai/atefr/skills/niri-ipc)
- [ClawHub publisher profile](https://clawhub.ai/user/atefr)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON IPC examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or forward JSON replies and event-stream lines from Niri IPC commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
