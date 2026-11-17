## Description:

Openclaw Task Reminder helps OpenClaw agents create, list, and manage prioritized tasks for tracking to-dos and important work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to maintain a simple local task list for OpenClaw workflows, including adding tasks, reviewing pending work by priority, marking tasks complete, and clearing completed items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task text is stored locally in plaintext.

Mitigation: Avoid storing secrets, credentials, or sensitive notes in task descriptions.

Risk: Clearing completed tasks permanently removes those task records.

Mitigation: Review completed tasks before running the clear command.

Risk: The installation example uses an unpinned ClawHub installer invocation.

Mitigation: Prefer a pinned or verified installer version when available.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yang1002378395-cmyk/skills/openclaw-task-reminder)
- [OpenClaw Installation Service](https://yang1002378395-cmyk.github.io/openclaw-install-service/)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Configuration]

**Output Format:** [Command-line text output and local JSON task storage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores task descriptions, priorities, statuses, and timestamps in a local plaintext tasks.json file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
