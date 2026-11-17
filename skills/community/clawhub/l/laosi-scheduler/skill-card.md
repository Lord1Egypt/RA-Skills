## Description:

Scheduler Pro helps agents define and manage local scheduled tasks, reminders, recurring jobs, cron-style schedules, and next-run calculations with persistent JSON storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to maintain a lightweight local registry of scheduled tasks, reminders, system maintenance jobs, monitoring checks, reports, and workflow triggers. It is suited to simple scheduling support rather than acting as a full cron executor.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is a simple local task registry and may be mistaken for a full cron executor.

Mitigation: Use it for lightweight reminders and schedule tracking, and rely on a production scheduler when exact execution semantics are required.

Risk: Task names, reminder text, and operational details may be stored in local plaintext JSON.

Mitigation: Avoid storing sensitive content unless local plaintext storage is acceptable for the deployment environment.

Risk: Deleting or toggling tasks changes the local schedule registry.

Mitigation: Confirm destructive or state-changing mutations before applying them.

## Reference(s):

- [Scheduler Pro ClawHub listing](https://clawhub.ai/534422530/skills/laosi-scheduler)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with Python code examples and cron schedule tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local scheduling guidance and sample Python code; persisted task data is stored in local JSON when the implementation is used.]

## Skill Version(s):

2.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
