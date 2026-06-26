## Description: <br>
Automated meeting preparation and daily commit summaries for development teams that check Google Calendar, summarize GitHub commits, and format developer-friendly updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hougangdev](https://clawhub.ai/user/hougangdev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to prepare for upcoming meetings by checking calendar events with video links and summarizing recent GitHub commits into standup or end-of-day updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Calendar and repository tokens can expose sensitive schedules, meeting links, and source-code activity. <br>
Mitigation: Use read-only Calendar access where possible, fine-grained GitHub tokens limited to required repositories, and protect local credential files. <br>
Risk: Broad calendar or repository configuration may include meetings, repositories, or developers outside the intended scope. <br>
Mitigation: Explicitly configure which calendars, repositories, and developers are included before running meeting prep or daily summaries. <br>
Risk: Recurring checks and daily summaries may send private meeting or commit details to an unintended destination. <br>
Mitigation: Enable scheduled checks only after confirming the summary destination and reviewing what information will be sent. <br>


## Reference(s): <br>
- [Google Calendar events API endpoint used by the skill](https://www.googleapis.com/calendar/v3/calendars/primary/events?timeMin=$NOW&timeMax=$LATER&singleEvents=true) <br>
- [GitHub organization repositories API endpoint used by the skill](https://api.github.com/orgs/ORG_NAME/repos?per_page=50&sort=pushed) <br>
- [GitHub commits API endpoint used by the skill](https://api.github.com/repos/ORG/REPO/commits?since=$SINCE&per_page=30) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text summaries with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configured calendar events, GitHub commit history, and local state files when enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
