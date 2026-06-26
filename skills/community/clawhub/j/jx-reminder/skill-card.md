## Description: <br>
Natural-language reminder secretary: capture events into git-synced workspace (data/logic separated), schedule Telegram reminders via SkillBoss cron, and answer "what's coming up" queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and workspace users use this skill to capture meetings, birthdays, deadlines, and other plans in natural language, store them in a workspace events file, schedule Telegram reminders, and query upcoming events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reminder details may contain sensitive personal scheduling information and are stored in the user's SkillBoss workspace. <br>
Mitigation: Avoid entering highly sensitive appointments unless the user trusts the workspace sync settings and related SkillBoss services. <br>
Risk: Event text and timing may be sent through SkillBoss and Telegram-related infrastructure to parse and deliver reminders. <br>
Mitigation: Use only with reminder content appropriate for those services and review ambiguous dates or times before scheduling. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kirkraman/jx-reminder) <br>
- [SkillBoss Pilot API endpoint](https://api.skillbossai.com/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, API calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown and concise natural-language responses with configuration values, JSON-like event details, and API call guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY; stores reminder events in a workspace YAML file and schedules Telegram reminder jobs.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
