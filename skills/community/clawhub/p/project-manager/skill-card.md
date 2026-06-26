## Description: <br>
Manage internal projects with JSON-based tasks, Kanban status updates, David notifications, and Apple Reminders synchronization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fr0ziii](https://clawhub.ai/user/fr0ziii) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and project operators use this skill to inspect and update Vivi OS project tasks stored in a JSON Kanban workflow, including approvals, blocked/review notifications, and optional Apple Reminders sync. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task text may expose sensitive internal project details when stored in the configured local JSON file or synchronized externally. <br>
Mitigation: Install only when the configured project path and Apple Reminders account are intended, and avoid storing secrets in task text. <br>
Risk: Move and sync actions can trigger Apple Reminders updates or chat notifications to David. <br>
Mitigation: Review add, move, and sync requests before asking the agent to perform them, especially for review and blocked transitions. <br>
Risk: Business rules can affect prioritization, approval flow, and work-in-progress limits. <br>
Mitigation: Require explicit approval before moving tasks to review and enforce the documented limit of three in-progress tasks. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fr0ziii/project-manager) <br>
- [Source skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown task summaries with JSON task updates and optional action requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update the configured project task JSON, request Apple Reminders sync, and notify David when tasks move to review or blocked.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
