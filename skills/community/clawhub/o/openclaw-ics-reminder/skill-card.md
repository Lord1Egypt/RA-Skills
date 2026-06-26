## Description: <br>
Helps agents create, list, cancel, and rotate ICS-backed calendar reminders through a configured reminder API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Cute-angel](https://clawhub.ai/user/Cute-angel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and agents use this skill to turn reminder requests into calendar-feed reminders, inspect or cancel existing reminders, and rotate a feed token when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A reminder API endpoint could receive reminder content and bearer-token authenticated requests. <br>
Mitigation: Use only a reminder API endpoint you trust and keep REMINDER_API_TOKEN private. <br>
Risk: Delete requests can cancel existing reminders. <br>
Mitigation: Review reminder IDs and user intent before running delete operations. <br>
Risk: Feed-token rotation can invalidate an existing subscribed calendar feed. <br>
Mitigation: Confirm rotation intent before rotating and update affected calendar subscriptions afterward. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Cute-angel/openclaw-ics-reminder) <br>
- [API Contract](references/api-contract.md) <br>
- [OpenClaw Config](references/openclaw-config.md) <br>
- [Time Parsing Rules](references/time-parsing-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON request or response bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js plus REMINDER_API_TOKEN and REMINDER_API_BASE_URL environment variables.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
