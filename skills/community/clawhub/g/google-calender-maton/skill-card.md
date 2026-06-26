## Description: <br>
Create, update, list, and delete Google Calendar events with support for attendees, time zones, and Google Meet through Maton API key authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[otman-ai](https://clawhub.ai/user/otman-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to manage Google Calendar events through Maton, including creating meetings, changing schedules, inviting attendees, and adding Google Meet links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Maton API key for Google Calendar access. <br>
Mitigation: Install only when use of a Maton API key is acceptable, store the key securely, and avoid exposing it in logs or shared prompts. <br>
Risk: Calendar write actions can create, update, reschedule, invite attendees to, or delete events. <br>
Mitigation: Before running write actions, confirm the target calendar, event ID, time zone, attendee emails, and whether invitations or update notifications should be sent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/otman-ai/google-calender-maton) <br>
- [Maton Google Calendar gateway](https://gateway.maton.ai/google-calendar/calendar/v3) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with curl examples and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses MATON_API_KEY authentication and IANA time zones for calendar operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
