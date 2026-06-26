## Description: <br>
Run programs that survive OpenClaw exec session cleanup and gateway restarts via tmux for long-running servers, tunnels, coding agents, and other persistent processes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[darwin7381](https://clawhub.ai/user/darwin7381) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to keep selected long-running commands alive across exec cleanup, session timeouts, and gateway restarts. It is most useful for dev servers, tunnels, background workers, builds, REPLs, and coding agents that should remain available after the current shell session ends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent tmux sessions can keep user-chosen processes running after the visible exec session ends. <br>
Mitigation: List and stop tmux sessions when work is complete, and use the dedicated socket convention to keep these sessions separate from a user's normal tmux environment. <br>
Risk: Tunnels such as ngrok, cloudflared, or localhost.run can expose local services beyond the local machine. <br>
Mitigation: Before starting a tunnel, confirm the service does not expose private data, admin panels, credentials, or unauthenticated write actions, and stop the session when finished. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/darwin7381/openclaw-tmux-persistent-process) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides tmux command patterns for starting, monitoring, interacting with, and stopping persistent sessions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
