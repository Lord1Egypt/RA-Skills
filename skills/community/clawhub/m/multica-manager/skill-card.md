## Description:

Multica Manager helps an agent coordinate Multica task assignment, progress monitoring, control actions, and result summaries across named worker agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andy-gaoyue](https://clawhub.ai/user/andy-gaoyue)

### License/Terms of Use:

MIT-0

## Use Case:

Developers or operators using Multica can use this skill to coordinate work among named agents, issue tasks, check status, and summarize completed results for a user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases can create tasks, stop or restart work, or send cross-session messages without clear confirmation.

Mitigation: Require explicit user confirmation and a specific agent, task title, and action before issuing Multica control commands or fallback session messages.

Risk: Task titles, messages, and logs may expose sensitive user or business data.

Mitigation: Avoid sensitive data in task titles and logs, and review task messages before sending them to other agents.

Risk: Result summaries may overstate completion if issue comments or agent status are stale or incomplete.

Mitigation: Check current issue status and agent state before reporting completion, and label uncertain or missing outputs clearly.

## Reference(s):

- [Multica Manager ClawHub release](https://clawhub.ai/andy-gaoyue/skills/multica-manager)
- [Skill source artifact](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Multica CLI commands, task status summaries, issue records, control recommendations, and fallback session messages.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
