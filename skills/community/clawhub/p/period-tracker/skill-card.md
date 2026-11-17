## Description:

经期管理 / Period Tracker helps an agent record menstrual periods and symptoms, predict cycles and ovulation windows, set reminders, generate health statistics, and export local data through natural-language guided commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sosshuai](https://clawhub.ai/user/sosshuai)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill with an agent to maintain a local reproductive-health log, ask for cycle and ovulation predictions, manage reminders, review statistics, and export their data. Agents use the skill's scripts and guidance to translate natural-language requests into period-tracking actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores sensitive reproductive-health information in a local plaintext JSON file.

Mitigation: Use it only on trusted devices, keep the data directory permissions restricted, and avoid recording unnecessary sensitive details.

Risk: Reminder setup modifies local cron entries.

Mitigation: Review reminder commands before applying them and inspect or remove period-tracker cron entries when reminders are no longer wanted.

Risk: The skill includes a built-in update command with weak disclosure and safety controls.

Mitigation: Prefer platform-managed updates and review the source and security verdict before running a forced update.

## Reference(s):

- [Period Tracker data schema](references/data-schema.md)
- [ClawHub skill page](https://clawhub.ai/sosshuai/skills/period-tracker)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown or plain-text agent responses with shell commands and optional JSON or CSV exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains a local JSON health log and can configure cron-based reminders.]

## Skill Version(s):

1.2.0 (source: server release evidence; script constant reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
