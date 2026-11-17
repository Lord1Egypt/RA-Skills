## Description:

Manage projects, tasks, schedules, custom fields, and team collaboration in Motion. Create projects, manage recurring tasks, configure workspaces, track statuses, and handle team scheduling with timezone-aware work hours.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External Motion users and teams use this skill to inspect workspaces, projects, tasks, schedules, statuses, users, comments, and custom fields, and to perform confirmed project, task, and custom-field updates through ClawLink.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawLink stores or brokers Motion credentials and can access Motion data available to the connected account.

Mitigation: Install only after confirming the user trusts ClawLink and the ClawHub plugin source.

Risk: Creates, updates, deletes, unassignments, and custom-field changes can modify or permanently remove Motion data.

Mitigation: Preview and confirm the target resource and intended effect before executing any write or destructive action.

## Reference(s):

- [Motion API Documentation](https://motion.app/developers)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/motion-planning)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs guide agent use of ClawLink-hosted Motion tools; write and destructive actions require explicit user confirmation.]

## Skill Version(s):

1.0.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
