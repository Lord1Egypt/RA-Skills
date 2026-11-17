## Description:

Health reminder assistant for medication reminders, water intake tracking, and activity prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this local command-line skill to track medication reminder entries, log water intake, and view activity prompts. It is not intended for medical diagnosis, prescription management, or device integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Medication names, schedules, and water logs are stored as plaintext JSON files under ~/.health-reminder.

Mitigation: Use the skill only on trusted user accounts, restrict the data directory on shared systems, and manually delete ~/.health-reminder when the stored records should be removed.

Risk: The skill supports reminders and tracking only; it does not provide medical diagnosis, prescription management, or device integration.

Mitigation: Use it as a personal reminder aid and rely on qualified healthcare guidance or clinical systems for medical decisions and prescription changes.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text command-line guidance and status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script stores local JSON records under ~/.health-reminder.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
