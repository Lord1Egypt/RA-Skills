## Description:

KAI-OS helps agents configure a digital-butler workspace with self-awareness, persistent memory, task scheduling, continuous improvement, and knowledge-network patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanyview1](https://clawhub.ai/user/wanyview1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use KAI-OS to structure AI assistant identity, user context, memory files, heartbeat schedules, and multi-agent collaboration workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead agents to store user information and long-term memory in workspace markdown files.

Mitigation: Require explicit user opt-in for memory storage, keep memory files scoped to the workspace, and provide a clear review and deletion process.

Risk: Recurring email, calendar, and task checks can expose private data or trigger unwanted external actions.

Mitigation: Use narrow read-only permissions where possible and require user confirmation before sending, modifying, or deleting anything.

Risk: Autonomous scheduling and continuous evolution behaviors may drift beyond the user's intended boundaries.

Mitigation: Define allowed tasks in HEARTBEAT.md and review scheduled behaviors before enabling recurring execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wanyview1/skills/kaios)
- [Kai-OS GitHub Project](https://github.com/wanyview1/Kai-OS)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and file-structure examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workspace file patterns such as SOUL.md, USER.md, MEMORY.md, HEARTBEAT.md, and daily memory notes.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
