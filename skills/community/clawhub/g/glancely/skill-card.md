## Description: <br>
Personal tracker framework that scaffolds habit, workout, mood, reminder, diary, and task trackers from natural language with a local dashboard and optional scheduled prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[junjieyu95](https://clawhub.ai/user/junjieyu95) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
End users and agent operators use Glancely to create and operate personal trackers for habits, mood, reminders, diary logging, and most-important-task check-ins. The skill helps an agent propose tracker schemas, run scaffold commands after confirmation, log entries, build a dashboard, and optionally register scheduled prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores personal tracker data locally, including potentially sensitive mood, diary, task, and reminder details. <br>
Mitigation: Use a trusted local machine, limit what sensitive details are logged, and protect the Glancely data directory with normal device and filesystem access controls. <br>
Risk: Diary logging can require Google Calendar OAuth credentials and token storage. <br>
Mitigation: Use a user-owned OAuth client, store credentials only in the expected Glancely credentials directory, and revoke Google access if the tracker is no longer used. <br>
Risk: Generated or discovered components under the local components directory can affect dashboard output, local storage, and scheduled prompts. <br>
Mitigation: Review generated components before use and avoid installing or running untrusted component files under ~/.glancely/components. <br>
Risk: Scheduled OpenClaw prompts may create recurring agent activity. <br>
Mitigation: Review cron schedules and notification text before enabling them, and disable unwanted schedules in the OpenClaw configuration. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/junjieyu95/glancely) <br>
- [Component Contract](docs/component-contract.md) <br>
- [Dashboard Date-Grid Overhaul Plan](docs/superpowers/plans/2026-05-10-dashboard-date-grid-overhaul.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated tracker files/configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local tracker components, SQLite migrations, dashboard files, and OpenClaw cron configuration under the user's Glancely data directory.] <br>

## Skill Version(s): <br>
0.3.0 (source: SKILL.md frontmatter, pyproject.toml, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
