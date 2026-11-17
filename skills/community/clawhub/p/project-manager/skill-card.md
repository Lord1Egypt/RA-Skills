## Description:

Manage internal projects with JSON-based tasks, Kanban status moves, Apple Reminders sync, and chat notifications for review or blocked work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fr0ziii](https://clawhub.ai/user/fr0ziii)

### License/Terms of Use:


## Use Case:

Developers and internal project operators use this skill to list, create, move, and synchronize project tasks in a JSON-backed Kanban workflow. It is intended for teams that use the configured project task file, Apple Reminders synchronization, and David chat notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task titles or details may be synced to Apple Reminders or included in chat notifications.

Mitigation: Avoid putting secrets or highly confidential details in tasks that may be synced or messaged.

Risk: The workflow reads and updates a specific projects.json task file path.

Mitigation: Install only when the configured task file path and project workflow match the intended environment.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Markdown text with JSON task updates when applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger Apple Reminders sync for opted-in tasks and chat notifications for review or blocked status changes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
