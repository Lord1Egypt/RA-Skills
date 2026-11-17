## Description:

Todoist task management for OpenClaw. Unified todo API with multi-agent identity, scheduled checks and reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kings0527](https://clawhub.ai/user/kings0527)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and agents use this skill to create, inspect, update, complete, delete, classify, and synchronize Todoist tasks. It separates personal reminders from agent-internal work and can synchronize task state into local workspace files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Todoist token to read and modify tasks, including create, update, complete, and delete operations.

Mitigation: Install only with a Todoist token scoped to acceptable projects and avoid shared or sensitive task spaces unless access controls are reviewed.

Risk: The package includes task forwarding to DingTalk and broad reminder routing.

Mitigation: Review, disable, or remove the DingTalk push script and confirm where task titles and reminder details will be sent before use.

Risk: The scripts make persistent workspace changes, including TASK.md, HEARTBEAT.md, identity configuration, and Todoist synchronization state.

Mitigation: Review heartbeat setup and workspace file changes before enabling automatic synchronization, and keep manual content inside the documented preservation markers.

## Reference(s):

- [ClawHub Todoist Skill Page](https://clawhub.ai/kings0527/skills/openclaw-todoist)
- [Todoist REST API endpoint used by the skill](https://api.todoist.com/api/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls]

**Output Format:** [Markdown and plain text responses with shell command effects and local configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read from and write to Todoist tasks, local OpenClaw workspace files, and heartbeat/task synchronization state.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
