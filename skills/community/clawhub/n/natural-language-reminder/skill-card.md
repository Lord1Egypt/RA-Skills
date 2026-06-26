## Description: <br>
Set reminders using natural language. Automatically creates one-time cron jobs and logs to markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dvornikov-dev](https://clawhub.ai/user/dvornikov-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to turn natural-language reminder requests into scheduled one-time or recurring OpenClaw cron jobs, with reminder history recorded in a markdown file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes a pre-filled recipient configuration that could route reminder messages to the wrong Telegram account. <br>
Mitigation: Delete or replace config.env during installation and confirm TO, CHANNEL, TIMEZONE, and REMINDERS_FILE before creating reminders. <br>
Risk: Reminder text and delivery metadata may be stored locally or sent through the configured delivery channel. <br>
Mitigation: Avoid sensitive reminder content until delivery is verified, and periodically review the reminder log and created cron jobs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dvornikov-dev/natural-language-reminder) <br>
- [Time zone database reference](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Text confirmations, markdown reminder-log entries, shell command invocations, and environment configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates scheduled cron jobs through OpenClaw and stores reminder history in the configured reminders file.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
