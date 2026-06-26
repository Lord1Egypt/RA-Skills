## Description: <br>
Atomic node skill to create a Google Calendar event using the gog CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zvirb](https://clawhub.ai/user/zvirb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill when a user wants to schedule or create a Google Calendar event through the gog CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create a real Google Calendar event if the agent runs the gog command with incorrect or unintended details. <br>
Mitigation: Before execution, verify the event title, calendar, start and end time, timezone, attendees, and intent to write to the calendar. <br>
Risk: Incorrect time arguments can create an event at the wrong time. <br>
Mitigation: Use --summary for the title and --from and --to for time bounds, with RFC3339 timestamps or supported relative time values. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zvirb/google-calendar-create-event) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, text] <br>
**Output Format:** [Markdown guidance with CLI arguments and JSON result expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gog binary and user confirmation before calendar writes.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
