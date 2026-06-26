## Description: <br>
OpenClaw Session Guard helps manage long OpenClaw sessions by archiving high-context conversations at an 80% threshold, rotating to a new session, and supporting macOS LaunchAgent installation, status checks, and removal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tel18610240060-collab](https://clawhub.ai/user/tel18610240060-collab) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install, inspect, or uninstall automation that archives oversized main agent sessions and starts a lower-token handoff in a fresh session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs background macOS LaunchAgent automation that manages OpenClaw sessions automatically. <br>
Mitigation: Install it only when background session rotation is intended, then verify LaunchAgent status and uninstall it when automatic rotation is no longer needed. <br>
Risk: Recent chat snippets may be archived under ~/.openclaw/knowledge/session-archives and reused for handoff. <br>
Mitigation: Avoid using it with sessions that contain secrets unless redaction, cleanup, and stricter file permissions are added. <br>
Risk: The automation can rewrite active OpenClaw session state during rotation. <br>
Mitigation: Review the status output and active-session map after installation, and test on noncritical agents before relying on it for important work. <br>
Risk: The security guidance calls out a missing LaunchAgent plist template that should be verified before relying on installation. <br>
Mitigation: Confirm the required plist template is present and that install and uninstall scripts work in the target environment before enabling the LaunchAgent. <br>


## Reference(s): <br>
- [OpenClaw Session Guard Reference](artifact/reference.md) <br>
- [OpenClaw Session Guard on ClawHub](https://clawhub.ai/tel18610240060-collab/openclaw-session-guard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and operational status guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local archive, handoff, status, and LaunchAgent-related files when its scripts are installed or run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
