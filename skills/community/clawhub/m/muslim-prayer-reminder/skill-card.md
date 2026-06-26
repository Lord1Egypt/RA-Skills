## Description: <br>
Gets Islamic prayer times for worldwide locations and helps configure automated Salat reminders using AlAdhan prayer-time data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diepox](https://clawhub.ai/user/diepox) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External OpenClaw users use this skill to query daily prayer times by city, country, coordinates, or date and to set up recurring reminders before, at, and after prayer times. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated reminder setup can create persistent background jobs that continue checking prayer times and announcing reminders. <br>
Mitigation: Before enabling reminders, review the exact cron jobs, storage path for prayer_times.json, delivery behavior, and removal steps. <br>
Risk: Setup guidance includes optional Cloudflare WARP commands with system-wide networking impact. <br>
Mitigation: Run VPN or sudo networking commands only after confirming they are necessary and acceptable for the target host. <br>
Risk: Instructions that recreate reminder jobs without asking can change an agent's startup behavior. <br>
Mitigation: Do not add automatic job-recreation instructions to AGENTS.md unless the user explicitly approves that persistent behavior. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/diepox/muslim-prayer-reminder) <br>
- [AlAdhan Prayer Times API](https://aladhan.com/prayer-times-api) <br>
- [AlAdhan Calculation Methods](https://api.aladhan.com/v1/methods) <br>
- [Reminder Setup Guide](references/setup-reminders.md) <br>
- [Prayer Time Calculation Methods](references/methods.md) <br>
- [Example Cron Jobs](references/example-cron-jobs.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, optional JSON prayer-time data, and reminder messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May configure persistent scheduled reminder checks when the user enables automated reminders.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
