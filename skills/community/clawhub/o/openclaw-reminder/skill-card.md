## Description: <br>
Create one-time reminder tasks using OpenClaw cron. User specifies reminder time and task content in natural language via Discord, and the task result will be sent back through Discord. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skyan](https://clawhub.ai/user/skyan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users interacting through Discord use this skill to schedule one-time reminders through OpenClaw cron and receive the result back in the Discord conversation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reminder text is scheduled as a future main-session system event, so sensitive or action-oriented content could be reintroduced later as an instruction. <br>
Mitigation: Use the skill for simple low-risk reminders, avoid sensitive or action-oriented tasks, and prefer inert notification storage when that distinction matters. <br>
Risk: User-supplied task content is passed into cron setup, which can be unsafe if validation is skipped. <br>
Mitigation: Validate reminder text with scripts/sanitize-message.sh and reject dangerous characters, newlines, command substitution, and dangerous command prefixes before scheduling. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/skyan/openclaw-reminder) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Text with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a confirmation reply after creating a one-time reminder.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
