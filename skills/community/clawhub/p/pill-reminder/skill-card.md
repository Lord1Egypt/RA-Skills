## Description:

Sends scheduled medication reminders with tracking, supports multiple users, refill alerts, and generates adherence reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bgoodwinstudio](https://clawhub.ai/user/bgoodwinstudio)

### License/Terms of Use:

MIT-0

## Use Case:

External users and caregivers use this skill to schedule medication or supplement reminders, record took or missed-dose responses, monitor refill counts, and produce adherence reports for medical visits. It is for reminder and tracking support only, not medical advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Medication names, profile names, refill counts, and adherence replies may be exposed through configured chat channels.

Mitigation: Use private or tightly controlled channels, avoid broad group chats, and redact sensitive details before sharing configuration or logs.

Risk: The skill handles sensitive medication tracking without enough privacy controls or channel scoping.

Mitigation: Confirm channel membership and authorization before displaying configuration, logs, or medication reminders.

Risk: Reminder and missed-dose text could be mistaken for medical guidance.

Mitigation: Keep the not-medical-advice disclaimer visible and direct users to a doctor or pharmacist for medication decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bgoodwinstudio/skills/pill-reminder)
- [README](artifact/README.md)
- [Skill Instructions](artifact/SKILL.md)
- [Pill Configuration Template](artifact/pills-template.md)
- [Adherence Log Template](artifact/pill-log-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with plain-text chat replies, command examples, scheduled reminder messages, and generated adherence reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local pills.md and pill-log.md files and schedule per-dose reminders through cron.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
