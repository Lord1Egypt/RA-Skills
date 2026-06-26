## Description: <br>
OpenClaw Quickstart guides new OpenClaw users through eight practical onboarding tasks with progress checks and daily reminders until the tasks are complete. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heyuncoder](https://clawhub.ai/user/heyuncoder) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to learn core OpenClaw workflows by completing guided setup, memory, weather, report, reminder, browser, presentation, and skill-install tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner flagged that the skill can add persistent heartbeat and daily reminder behavior before explicit user approval. <br>
Mitigation: Review before installing, prefer the documented dry run, and confirm the reminder schedule and notification behavior before applying changes. <br>
Risk: The skill writes OpenClaw workspace state and progress files as part of onboarding. <br>
Mitigation: Run it in the intended OpenClaw workspace, inspect proposed file changes, and keep only the progress or configuration changes the user wants. <br>
Risk: The final task can install another third-party ClawHub skill. <br>
Mitigation: Review and scan any recommended third-party skill before installing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/heyuncoder/openclaw-quickstart) <br>
- [Initialize AI Identity](references/task-01-identity.md) <br>
- [Save Your Preferences](references/task-02-memory.md) <br>
- [Check the Weather](references/task-03-weather.md) <br>
- [Generate a Report](references/task-04-report.md) <br>
- [Set a Reminder](references/task-05-reminder.md) <br>
- [Browser Info Gathering](references/task-06-browser.md) <br>
- [Generate a PPT](references/task-07-ppt.md) <br>
- [Install a Skill from ClawHub](references/task-08-skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and progress JSON from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update OpenClaw workspace files and create recurring reminder behavior when installed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
