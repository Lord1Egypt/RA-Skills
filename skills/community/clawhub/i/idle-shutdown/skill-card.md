## Description: <br>
Monitors OpenClaw Gateway user session idleness and automatically shuts down the Gateway after a configured idle period. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yu200512](https://clawhub.ai/user/yu200512) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw Gateway operators use this skill to install and configure a lightweight idle watcher that stops the Gateway after sessions remain inactive beyond a configurable threshold. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs persistent user-level automation that can stop the OpenClaw Gateway without per-event confirmation. <br>
Mitigation: Enable it only when automatic idle shutdown is intended, review the service before installation, and disable it with systemctl --user disable --now openclaw-idle-watch.service when no longer needed. <br>
Risk: An overly short idle threshold or mismatched session activity check can stop the Gateway during active workflows. <br>
Mitigation: Set IDLE_SECONDS conservatively and confirm that the monitored session directory and transcript matching behavior reflect the target OpenClaw workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yu200512/idle-shutdown) <br>
- [Publisher profile](https://clawhub.ai/user/yu200512) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash commands and systemd service configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces installation, configuration, uninstallation, and lifecycle guidance for a persistent user-level idle watcher.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
