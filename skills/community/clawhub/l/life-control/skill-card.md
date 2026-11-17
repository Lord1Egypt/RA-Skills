## Description:

Orchestrate the Life Control CLI skill for OpenClaw agent fleets: initialize the Life Control database, register agent personas, wire Telegram bots, and run daily routines (Morning Alignment, Body Protocol, Financial Pulse, Social Radar, Work Priming, Shutdown).

This skill is ready for commercial/non-commercial use.

## Publisher:

[rachitsharma123](https://clawhub.ai/user/rachitsharma123)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw operators use this skill to set up and run a personal Life Control system that coordinates persona agents, daily routines, structured life-domain tracking, and Telegram notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to run setup, routine, notification, and cron scripts from a separate Life Control repository that were not bundled in the inspected artifact.

Mitigation: Review the referenced repository scripts before execution, especially bootstrap.sh, setup-agents.sh, telegram-sender.sh, routines, and cron templates.

Risk: The workflows can involve Telegram bot tokens, chat IDs, personal tracking data, local database writes, scheduled routines, and notifications.

Mitigation: Provide credentials and personal data only in a trusted environment after confirming where the database is stored and where notifications are sent.

## Reference(s):

- [Life Control ClawHub Skill Page](https://clawhub.ai/rachitsharma123/skills/life-control)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides database initialization, persona registration, routine execution, cron scheduling, and Telegram notification setup.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
