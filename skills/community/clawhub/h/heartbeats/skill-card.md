## Description:

Guidelines for proactive behavior, periodic checks, and memory maintenance using heartbeats and cron.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flayzz](https://clawhub.ai/user/flayzz)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users use Heartbeats to decide how to handle periodic heartbeat polls, batch non-urgent checks, and maintain workspace memory without unnecessary interruptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports broad proactive access to private data, persistent memory, and repository publishing without clear approval gates.

Mitigation: Install only where the agent is allowed to read connected personal sources and modify workspace memory, and require explicit approval before commits, pushes, external messages, HEARTBEAT.md edits, and MEMORY.md deletions or rewrites.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/flayzz/skills/heartbeats)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide an agent to create or update HEARTBEAT.md, MEMORY.md, and memory/heartbeat-state.json when workspace access allows it.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
