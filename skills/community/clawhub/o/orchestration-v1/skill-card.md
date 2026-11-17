## Description:

Orchestrates multi-agent teams with defined roles, task lifecycles, handoff protocols, review workflows, and artifact-sharing conventions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangjun20250818-cyber](https://clawhub.ai/user/zhangjun20250818-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to define sustained multi-agent workflows, route tasks across specialized agents, manage handoffs, and add review gates before work is accepted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security verdict is suspicious because the skill includes mismatched instructions for sending and confirming a browser chat message.

Mitigation: Review or remove the Physical Strike (Justin Protocol) before installation and require explicit, task-specific user confirmation of the destination and exact content before external messages, browser submissions, or screenshots.

Risk: Recurring operations guidance can create unintended repeated actions if schedules, triggers, or limits are ambiguous.

Mitigation: Configure recurring operations with clear times, triggers, scope, and stop conditions before use.

## Reference(s):

- [Team Setup](references/team-setup.md)
- [Task Lifecycle](references/task-lifecycle.md)
- [Communication](references/communication.md)
- [Patterns](references/patterns.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Configuration instructions]

**Output Format:** [Markdown guidance with templates, task-state examples, and workflow checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include role definitions, handoff instructions, task lifecycle rules, review protocols, and artifact path conventions.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
