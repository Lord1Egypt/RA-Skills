## Description: <br>
Notifies the current session user when an agent's model changes, with heartbeat checks, interrupted-message recovery, and SQLite-backed state storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wljmmx](https://clawhub.ai/user/wljmmx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to check model state before replies and notify users when the active model changes or when a previously interrupted notification should be resumed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently stores agent IDs, model names, channel/session IDs, and pending notification text across sessions. <br>
Mitigation: Use it only where that storage is acceptable, confirm SQLite file permissions, and document retention expectations before deployment. <br>
Risk: The artifact writes to a hard-coded local OpenClaw data path that may not match the installing user or documented location. <br>
Mitigation: Patch the database path to the current user's OpenClaw data directory before installing or running the script. <br>


## Reference(s): <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [ClawHub skill page](https://clawhub.ai/wljmmx/model-switch-notify) <br>
- [Publisher profile](https://clawhub.ai/user/wljmmx) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration] <br>
**Output Format:** [JSON status objects, notification text, and Markdown usage guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local SQLite database to persist agent model state and pending notifications.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
