## Description: <br>
Heartbeat Manager monitors agent task state, recurring checklists, upcoming events, timeouts, reports, and health scores while optionally syncing notifications and workspace changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zeron-G](https://clawhub.ai/user/zeron-G) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to run scheduled heartbeat checks, maintain task status files, surface overdue work, and generate daily or weekly status reports. It is intended for OpenClaw-style agent workspaces that need local task monitoring with optional email, Canvas, FSP, Discord, and Git integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports that this release ships with automatic Git push enabled. <br>
Mitigation: Disable git.enabled, git.auto_commit, and git.auto_push unless the operator explicitly wants heartbeat runs to commit and push workspace changes to a configured remote. <br>
Risk: The security review reports an undisclosed Discord notification path that can reuse an existing OpenClaw token. <br>
Mitigation: Set discord_notify.enabled to false unless Discord posting is intended, and avoid relying on shared ~/.openclaw credentials for this skill. <br>
Risk: Email, Canvas, and FSP integrations can read external service data and rewrite workspace status files when credentials are configured. <br>
Mitigation: Configure only the tokens required for the deployment, disable unused integrations, and review generated workspace changes before enabling automated Git synchronization. <br>


## Reference(s): <br>
- [Heartbeat Manager on ClawHub](https://clawhub.ai/zeron-G/heartbeat-manager) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [_meta.json](artifact/_meta.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown workspace files, JSON state files, command-line status text, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local workspace status files and logs; optional integrations may send notifications, read external service data, or commit and push workspace changes when enabled.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata, artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
