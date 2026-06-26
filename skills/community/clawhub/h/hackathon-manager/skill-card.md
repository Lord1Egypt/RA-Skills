## Description: <br>
Track hackathon deadlines, manage submission checklists, and monitor progress. Use when managing multiple hackathons, checking what's due soon, marking requirements complete, or extracting hackathon information from URLs to auto-populate deadlines and requirements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tonbistudio](https://clawhub.ai/user/tonbistudio) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, builders, and hackathon participants use this skill to track multiple hackathons, deadlines, prizes, and submission checklist progress. It can also help populate hackathon records from URLs and optionally synchronize tracked milestones to Google Calendar. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Google Calendar removal command can delete real calendar events too broadly because it matches event titles by hackathon name and deletes with force. <br>
Mitigation: Before running gcal remove, confirm the Google account and exact hackathon name, then review matching events with gcal list. <br>
Risk: Google Calendar synchronization modifies an authenticated external calendar through the gog CLI. <br>
Mitigation: Install and authenticate gog intentionally, and run synchronization only for calendars where creating hackathon milestone events is expected. <br>


## Reference(s): <br>
- [gog CLI](https://github.com/rubiojr/gog) <br>
- [Hackathon Manager on ClawHub](https://clawhub.ai/tonbistudio/hackathon-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-text status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes hackathon tracking data to a local JSON file and can call the external gog CLI for Google Calendar operations.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
