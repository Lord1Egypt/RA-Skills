## Description: <br>
Atomic node skill to delete a Google Calendar event using the gog CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zvirb](https://clawhub.ai/user/zvirb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents used by calendar users or operators use this skill to delete a specified Google Calendar event through the local gog CLI when a calendar ID and event ID are known. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delete the wrong Google Calendar event if the calendar ID or event ID is incorrect. <br>
Mitigation: Verify the calendar ID and event ID, and have the agent show the event details before deletion when accuracy matters. <br>


## Reference(s): <br>
- [Google Calendar Delete Event on ClawHub](https://clawhub.ai/zvirb/google-calendar-delete-event) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, text, guidance] <br>
**Output Format:** [Markdown or plain text with a gog calendar delete command and deletion confirmation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the local gog CLI and a target calendar ID and event ID.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
