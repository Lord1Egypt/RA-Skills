## Description: <br>
Reads enterprise Microsoft 365 Outlook calendar events and helps answer user questions about schedules, meetings, work items, tasks, and date ranges. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ilove323](https://clawhub.ai/user/ilove323) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and agents use this skill to retrieve Outlook Web calendar events for today, tomorrow, a week, a month, or a custom range, then summarize events, meeting duration, and schedule details in response to natural-language calendar questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores Microsoft 365 credentials, cookies, bearer tokens, and possible login screenshots on the local machine. <br>
Mitigation: Install only for trusted publishers, protect the local ~/.outlook directory, and delete or rotate stored secrets when access is no longer needed. <br>
Risk: The skill reuses browser cookies and bearer tokens to access Outlook Web calendar data. <br>
Mitigation: Prefer a version that uses official Microsoft OAuth or Microsoft Graph with a narrow calendar-read scope instead of password and cookie reuse. <br>
Risk: Broad activation for schedule, work, task, and meeting questions can expose calendar data when the user did not intend to run the skill. <br>
Mitigation: Narrow activation to explicit calendar requests and confirm with the user before retrieving calendar data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ilove323/outlook-calendar) <br>
- [Publisher profile](https://clawhub.ai/user/ilove323) <br>
- [Microsoft sign-in endpoint used by the skill](https://login.microsoftonline.com) <br>
- [Outlook calendar endpoint used by the skill](https://outlook.office.com/calendar/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown or JSON calendar summaries with optional shell commands for login and calendar retrieval] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Calendar event output may include subjects, start and end times, duration, status, organizer, and all-day markers.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
