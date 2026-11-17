## Description:

Provides a Markdown-based knowledge management system for AI agents, covering identity, user context, operating rules, tools, long-term memory, daily logs, learnings, scheduled review tasks, and multi-agent memory coordination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wujun2081](https://clawhub.ai/user/wujun2081)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create and maintain Markdown files for agent identity, user context, operating rules, tool notes, long-term memory, daily logs, learnings, and recurring maintenance tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist task details and conversation feedback into workspace memory and future agent rules without clear approval or redaction controls.

Mitigation: Use it only in workspaces where persistent logs and agent-rule updates are acceptable, and require manual approval before changes to AGENTS.md, SOUL.md, TOOLS.md, MEMORY.md, or HEARTBEAT.md.

Risk: Persistent memory files may capture secrets, personal data, customer data, or sensitive project context.

Mitigation: Define redaction and retention rules before use, and review memory updates before committing or sharing workspace files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wujun2081/skills/knowledge-system)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workspace file structure guidance and reusable Markdown templates for persistent agent memory.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
