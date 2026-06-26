## Description: <br>
Google Calendar: Show upcoming events across all calendars. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to ask an agent for upcoming Google Calendar agenda information from the gws CLI, with optional date range, calendar, and timezone filters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose private event details from all calendars by default. <br>
Mitigation: Use the intended Google account and pass --calendar when the agent should only view a specific calendar. <br>
Risk: The skill relies on the local gws CLI and its shared authentication setup. <br>
Mitigation: Install only when the gws CLI and generated shared auth instructions are trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/gws-calendar-agenda) <br>
- [Publisher profile](https://clawhub.ai/user/googleworkspace-bot) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Google Calendar agenda retrieval through the gws CLI; output may include private calendar details unless narrowed with --calendar.] <br>

## Skill Version(s): <br>
1.0.13 (source: ClawHub release evidence; artifact metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
