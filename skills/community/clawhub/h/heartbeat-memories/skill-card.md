## Description:

Heartbeat-Memories is a fully local long-term memory system for OpenClaw that organizes goals, experiences, emotions, sessions, and version history with optional semantic search and heartbeat recall.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jamieyang9996](https://clawhub.ai/user/jamieyang9996)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and agent developers use this skill to persist and retrieve structured local memory about goals, technical experience, emotions, sessions, and configuration history. It helps an agent recall prior context and personalize responses without relying on external APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to persist goals, emotions, habits, and conversation history, which can include sensitive personal or work context.

Mitigation: Review stored memory content regularly, avoid saving secrets or sensitive work data, and disable auto_record unless persistent memory is explicitly desired.

Risk: Heartbeat recall and automatic recording are broadly enabled in the provided configuration template.

Mitigation: Disable or lower heartbeat_recall and memory_system.auto_record settings before use if proactive reminders or broad memory capture are not appropriate.

Risk: Deletion commands in the documentation can remove local skill or memory data.

Mitigation: Back up memory data before running removal or reset commands.

Risk: Dependencies are specified with lower bounds rather than pinned exact versions.

Mitigation: Install in a virtual environment and pin reviewed dependency versions for managed deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jamieyang9996/skills/heartbeat-memories)
- [ClawHub publisher profile](https://clawhub.ai/user/jamieyang9996)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and text guidance with optional JSON configuration and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local Markdown memory files and local vector database state when its scripts are run.]

## Skill Version(s):

2.0.0 (source: ClawHub release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
