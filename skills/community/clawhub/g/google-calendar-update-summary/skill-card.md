## Description: <br>
Atomic node skill to exclusively update the summary (title) of a Google Calendar event. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zvirb](https://clawhub.ai/user/zvirb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to rename an existing Google Calendar event by changing only its summary or title. It is suited for workflows that already know the target calendar ID, event ID, and replacement title. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can rename the wrong calendar event if the agent uses an incorrect calendar ID or event ID. <br>
Mitigation: Confirm the exact calendar ID, event ID, and replacement title before running the gog command. <br>
Risk: The gog CLI may be authenticated to an unintended Google account. <br>
Mitigation: Verify gog authentication and target account context before updating an event. <br>
Risk: The command may fail or return an unexpected summary after execution. <br>
Mitigation: Check the returned JSON and retry only when the response does not confirm the requested summary. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zvirb/google-calendar-update-summary) <br>
- [Publisher profile](https://clawhub.ai/user/zvirb) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [JSON response from the Google Calendar CLI, with concise guidance for validating the updated summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gog CLI and an authenticated Google Calendar account; limited to updating the event summary.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
