## Description:

Multi-queue task orchestration system. Tasks are routed to queues by model source, with support for task dependencies, context passing, and failure handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bg1avd](https://clawhub.ai/user/bg1avd)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to queue agent tasks by model source, run one task at a time per source, pass context across dependencies, and monitor task completion or failure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install persistent background dispatch through heartbeat or cron behavior.

Mitigation: Require confirmation before first-run setup, narrow activation triggers, and review or disable heartbeat and cron integration before deployment.

Risk: Queued tasks may spawn agents from broad prompts and store task data locally.

Mitigation: Avoid queueing sensitive data unless local storage permissions and retention are approved, and review queued task prompts before dispatch.

## Reference(s):

- [Queue Schema Reference](artifact/queue-schema.md)
- [ClawHub skill page](https://clawhub.ai/bg1avd/skills/model-queue)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown responses with JSON queue files and setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates per-source FIFO queue files, archive files, heartbeat entries, and optional cron dispatch notifications.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
