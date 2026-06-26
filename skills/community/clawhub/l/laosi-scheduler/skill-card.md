## Description: <br>
Scheduler Pro helps agents create and manage local scheduled tasks, one-time reminders, and cron-style recurring jobs with persistent storage and next-run calculation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and productivity users use this skill to manage local task schedules for maintenance jobs, monitoring checks, report generation, and reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The cron parser is simplified and may not honor every schedule documented by the skill. <br>
Mitigation: Use it only for simple local reminders or task registries unless unsupported schedules are rejected clearly and the parser is validated for the intended cron patterns. <br>
Risk: Relying on this skill for important backups, alerts, or reports could cause missed or mistimed tasks. <br>
Mitigation: Use a production scheduler or external monitoring for critical workflows, and review next-run calculations before depending on generated schedules. <br>
Risk: Scheduled task records may be persisted locally in scheduled_tasks.json. <br>
Mitigation: Avoid storing secrets or sensitive task details in scheduled entries, and review the local storage path before deployment. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python code examples and cron expressions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist scheduled task records to scheduled_tasks.json when the included Python example is executed.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence, SKILL.md frontmatter, hub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
