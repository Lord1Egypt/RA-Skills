## Description: <br>
Create, list, cancel, and snooze reminders using OpenClaw cron jobs for one-shot or recurring reminders, with confirmation before changes and safe reminder text handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[martok9803](https://clawhub.ai/user/martok9803) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to schedule, review, cancel, and snooze reminders from natural-language requests while preserving timezone and recurrence details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reminder payloads may expose sensitive information if users include secrets or private content. <br>
Mitigation: Do not put passwords, tokens, access keys, or sensitive private content into reminder messages. <br>
Risk: Incorrect time, timezone, recurrence, or message text could create the wrong reminder. <br>
Mitigation: Review the confirmation details carefully before allowing the agent to create, update, cancel, or snooze a reminder. <br>
Risk: Recurring reminders can become spammy if scheduled too broadly or without clear consent. <br>
Mitigation: Require explicit confirmation before creating recurring reminders and avoid broadcasting to multiple targets unless the user explicitly requests it. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with cron tool call details and reminder payload text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reminder creation, update, cancellation, and snooze actions require user confirmation before execution.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
