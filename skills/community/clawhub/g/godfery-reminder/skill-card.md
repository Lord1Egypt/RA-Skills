## Description: <br>
Reminder captures natural-language events in Chinese or English, stores structured reminders in a workspace YAML file, schedules Telegram notifications through SkillBoss cron, and answers upcoming-plan queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[godferylindsay](https://clawhub.ai/user/godferylindsay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and SkillBoss users use this skill to capture meetings, birthdays, deadlines, and other plans from chat, persist reminders locally, schedule Telegram alerts, and ask for upcoming events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reminder text may contain sensitive personal or work information that is processed by SkillBoss and stored in a local workspace YAML file. <br>
Mitigation: Install only when that data flow is acceptable, keep secrets out of committed files, and review local reminder data before syncing or sharing the workspace. <br>
Risk: Incorrect timezone, ambiguous natural-language dates, or notification offsets can create reminders at the wrong time. <br>
Mitigation: Confirm resolved dates and times, configure REMINDER_TZ and REMINDER_OFFSETS_MINUTES deliberately, and ask clarifying questions for ambiguous events. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/godferylindsay/godfery-reminder) <br>
- [SkillBoss setup guide](https://skillboss.co/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown responses with structured reminder details, YAML event updates, and scheduling guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local reminder data and schedule Telegram notifications when the host agent provides those capabilities.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
