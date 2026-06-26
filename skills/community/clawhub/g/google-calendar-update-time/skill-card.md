## Description: <br>
Atomic node skill to exclusively update the start and end time of a Google Calendar event. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zvirb](https://clawhub.ai/user/zvirb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to reschedule an existing Google Calendar event by changing only its start and end times through the gog CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change calendar event times when invoked with the user's configured Google account. <br>
Mitigation: Confirm the calendar ID, event ID, start time, and end time before allowing the agent to run the gog update command. <br>
Risk: A malformed or unintended update could reschedule the wrong event or set incorrect times. <br>
Mitigation: Validate the returned JSON response and confirm the start and end fields match the requested values. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zvirb/google-calendar-update-time) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, json, guidance] <br>
**Output Format:** [JSON command specification and final JSON event update response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gog CLI and an existing calendar ID, event ID, start time, and end time.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
