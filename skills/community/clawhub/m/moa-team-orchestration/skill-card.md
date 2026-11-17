## Description:

Orchestrates multi-agent teams with defined roles, task lifecycles, handoff protocols, and review workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[admirobot](https://clawhub.ai/user/admirobot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up sustained multi-agent workflows, route tasks through review, manage handoffs, and keep shared artifacts discoverable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Multi-agent work can lose artifacts or context when output paths and handoff instructions are unclear.

Mitigation: Require exact shared output paths, handoff summaries, verification steps, and known-issue notes for every spawned task.

Risk: Agent teams can produce quality drift if builders approve their own work or review steps are skipped.

Mitigation: Route completed work through a separate reviewer or orchestrator review before marking tasks done.

Risk: Scheduled operations or dispatch loops may make changes without sufficient oversight.

Mitigation: Define agent read/write boundaries, shared artifact locations, and human approval requirements for scheduled ops before use.

## Reference(s):

- [Team Setup](references/team-setup.md)
- [Task Lifecycle](references/task-lifecycle.md)
- [Communication](references/communication.md)
- [Patterns](references/patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown guidance with structured templates and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
