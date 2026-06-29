## Description: <br>
Google Calendar API integration with managed OAuth for creating events, listing calendars, checking availability, and managing schedules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to operate Google Calendar through Maton-managed OAuth: view calendars and events, check free/busy availability, and perform calendar changes after explicit approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, and delete events in connected Google Calendar accounts. <br>
Mitigation: Require explicit user approval before write operations and confirm the target calendar, event details, attendees, and intended effect. <br>
Risk: Requests may affect the wrong Google account when multiple calendar connections are active. <br>
Mitigation: Specify the intended connection ID whenever more than one active Google Calendar connection exists. <br>
Risk: Calendar access depends on a Maton API key and OAuth-backed network requests. <br>
Mitigation: Keep MATON_API_KEY protected, verify authentication state before use, and limit use to expected operator workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/skills/google-calendar-api) <br>
- [Google Calendar API Overview](https://developers.google.com/calendar/api/v3/reference) <br>
- [Google Calendar CalendarList: list](https://developers.google.com/workspace/calendar/api/v3/reference/calendarList/list) <br>
- [Google Calendar Events: list](https://developers.google.com/workspace/calendar/api/v3/reference/events/list) <br>
- [Google Calendar Events: insert](https://developers.google.com/workspace/calendar/api/v3/reference/events/insert) <br>
- [Google Calendar Freebusy: query](https://developers.google.com/workspace/calendar/api/v3/reference/freebusy/query) <br>
- [Maton CLI Manual](https://cli.maton.ai/manual) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with command examples, HTTP request paths, and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a configured Google Calendar OAuth connection.] <br>

## Skill Version(s): <br>
1.0.8 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
