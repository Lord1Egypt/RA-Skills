## Description: <br>
Google Calendar API integration with managed OAuth for creating events, listing calendars, checking availability, and managing schedules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to interact with Google Calendar through Maton-managed OAuth, including reading calendars and events, creating or updating events, deleting events, and querying free/busy availability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive MATON_API_KEY and access to a connected Google Calendar account. <br>
Mitigation: Keep MATON_API_KEY private, install only if Maton is trusted for the calendar workflow, and revoke unused OAuth connections. <br>
Risk: Calendar write operations can create, update, or delete events in the connected account. <br>
Mitigation: Confirm the target calendar, connection, resource, and intended effect before executing any create, update, or delete request. <br>
Risk: Multiple Google Calendar connections can route requests to the wrong account if the connection is omitted. <br>
Mitigation: Specify the intended Maton connection whenever multiple Google accounts are linked. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/google-calendar-api) <br>
- [Google Calendar API Overview](https://developers.google.com/calendar/api/v3/reference) <br>
- [Calendar List: list](https://developers.google.com/workspace/calendar/api/v3/reference/calendarList/list) <br>
- [Events: list](https://developers.google.com/workspace/calendar/api/v3/reference/events/list) <br>
- [Events: insert](https://developers.google.com/workspace/calendar/api/v3/reference/events/insert) <br>
- [Events: update](https://developers.google.com/workspace/calendar/api/v3/reference/events/update) <br>
- [Events: delete](https://developers.google.com/workspace/calendar/api/v3/reference/events/delete) <br>
- [Free/busy: query](https://developers.google.com/workspace/calendar/api/v3/reference/freebusy/query) <br>
- [Maton CLI Manual](https://cli.maton.ai/manual) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash, Python, JavaScript, HTTP, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and an active Google Calendar OAuth connection through Maton.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
