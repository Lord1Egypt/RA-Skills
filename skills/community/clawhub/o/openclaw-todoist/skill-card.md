## Description: <br>
Todoist task management for OpenClaw. Unified todo API with multi-agent identity, scheduled checks and reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kings0527](https://clawhub.ai/user/kings0527) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agents use this skill to create, categorize, and synchronize Todoist tasks, including personal reminders and agent-internal task tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a Todoist token under ~/.openclaw/workspace. <br>
Mitigation: Install only in environments where local token storage is acceptable, restrict file access, and remove or rotate the token when no longer needed. <br>
Risk: The skill can update local workspace task and heartbeat files. <br>
Mitigation: Review TASK.md and HEARTBEAT.md changes after setup or synchronization, especially in shared workspaces. <br>
Risk: The bundled push script can send Todoist task text to a hardcoded DingTalk target. <br>
Mitigation: Remove or disable scripts/push-todo.sh unless that DingTalk delivery path is explicitly intended and approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kings0527/openclaw-todoist) <br>
- [Todoist REST API endpoint](https://api.todoist.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can update local TASK.md and HEARTBEAT.md files and call Todoist API endpoints when configured with a user token.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
