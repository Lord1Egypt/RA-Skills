## Description:

Natural-language reminder secretary that captures events from Chinese or English chat, saves structured reminder data in a workspace file, schedules Telegram reminders through SkillBoss cron, and answers upcoming-plan queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godferylindsay](https://clawhub.ai/user/godferylindsay)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and teams use this skill to turn natural-language schedule notes into saved reminders, Telegram notifications, and quick summaries of upcoming meetings, birthdays, deadlines, and plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reminder text may contain private personal or work schedule information and can be sent to SkillBoss's API for parsing.

Mitigation: Review sensitive reminder text before use and install only if sending that content to SkillBoss for parsing is acceptable.

Risk: The skill can create persistent cron notifications and write reminder records after resolving event details.

Mitigation: Confirm the resolved event, timezone, reminder offsets, and notification schedule before allowing file writes or cron job creation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/godferylindsay/skills/godfery-reminder)
- [SkillBoss Setup Guide](https://skillboss.co/skill.md)

## Skill Output:

**Output Type(s):** [text, yaml, shell commands, configuration]

**Output Format:** [Concise natural-language responses with structured YAML reminder records and cron scheduling actions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default reminder offsets are 24 hours, 1 hour, and 10 minutes before the event unless configured otherwise.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
