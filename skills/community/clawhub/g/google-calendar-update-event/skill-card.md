## Description: <br>
Atomic node skill to update a Google Calendar event using the gog CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zvirb](https://clawhub.ai/user/zvirb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when an existing Google Calendar event needs to be modified or rescheduled through the local gog CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify real Google Calendar events through the authenticated gog CLI account. <br>
Mitigation: Confirm the intended Google account, calendarId, eventId, and proposed event changes before running update commands. <br>
Risk: A wrong event identifier or time range can reschedule the wrong calendar entry. <br>
Mitigation: Ask the agent to present the exact command and event fields for review before important updates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zvirb/google-calendar-update-event) <br>
- [Publisher profile](https://clawhub.ai/user/zvirb) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples and JSON command/output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the local gog CLI and Google Calendar authentication for the intended account.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
