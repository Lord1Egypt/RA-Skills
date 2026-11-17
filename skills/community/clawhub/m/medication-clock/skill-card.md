## Description:

Medication Clock helps users create Euthyrox medication reminders, record doses, review adherence, and export local medication records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robbingithub](https://clawhub.ai/user/robbingithub)

### License/Terms of Use:

MIT-0

## Use Case:

External users who need medication adherence support can use this skill to receive reminders, confirm Euthyrox doses, review status and history, generate adherence reports, and export records for personal review or sharing with a clinician.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release metadata grants broad command execution authority.

Mitigation: Review or remove execute_command permission before installation unless command execution is required and appropriately scoped.

Risk: The test script and cleanup mode can change real medication records in the user's OpenClaw data directory.

Mitigation: Avoid running test_system.py or test_system.py --cleanup against a real profile; use disposable data or back up ~/.openclaw/medication_data first.

Risk: Medication records and CSV exports contain sensitive health-related data stored locally.

Mitigation: Restrict filesystem access to ~/.openclaw/medication_data and treat exported CSV files as sensitive personal data.

Risk: Automated reminders depend on manual OpenClaw cron and channel configuration.

Mitigation: Confirm the reminder channel and cron configuration before relying on the skill for medication reminders.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/robbingithub/skills/medication-clock)
- [README](artifact/README.md)
- [User Guide](artifact/USER_GUIDE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, CSV files]

**Output Format:** [Markdown-style text responses, shell command examples, JSON-backed local records, and CSV exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores medication records, settings, statistics, and CSV exports locally under ~/.openclaw/medication_data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
