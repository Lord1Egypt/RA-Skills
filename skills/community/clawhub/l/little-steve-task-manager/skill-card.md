## Description:

Little Steve Task Manager is a lightweight IM-native task system for quick task operations in chat, with daily summaries and automatic status updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[echoofzion](https://clawhub.ai/user/echoofzion)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to manage task lists directly in chat workflows, including adding tasks, listing by status, updating priority or status, and marking work complete.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores task data in local JSON files, so task titles and metadata may expose sensitive operational details to anyone with filesystem access.

Mitigation: Keep the skill data directory writable only by trusted accounts and avoid storing secrets or highly sensitive details in tasks.

Risk: The task script performs local file writes and temporary-file replacement as part of normal operation.

Mitigation: Run the skill as an unprivileged user and review filesystem permissions before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/echoofzion/skills/little-steve-task-manager)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and task-list text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local JSON task and settings files; requires jq for command execution.]

## Skill Version(s):

0.1.7 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
