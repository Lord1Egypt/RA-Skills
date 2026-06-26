## Description: <br>
Manage the meeting lifecycle by scheduling through Google Calendar, suggesting time slots, preparing briefs, generating agendas, and creating follow-up tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nollio](https://clawhub.ai/user/nollio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and professionals use this skill to coordinate meetings, manage availability, prepare for calls, create agendas, and capture follow-up actions from meeting notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Google Calendar and optional Gmail access can expose sensitive schedule, attendee, and email context. <br>
Mitigation: Grant only acceptable gog permissions and disable include_email_context when email context is not needed. <br>
Risk: Web search can use attendee and company names from calendar events. <br>
Mitigation: Review config/settings.json before use and disable include_web_search for private or sensitive meetings. <br>
Risk: Local meeting notes and exported agendas may contain attendee names, decisions, action items, and business context. <br>
Mitigation: Keep the notes directory and exported files private, and periodically review or delete retained meeting records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nollio/meeting-scheduler-pro) <br>
- [Publisher profile](https://clawhub.ai/user/nollio) <br>
- [README](artifact/README.md) <br>
- [Security considerations](artifact/SECURITY.md) <br>
- [Default settings](artifact/config/settings.json) <br>
- [Dashboard specification](artifact/dashboard-kit/DASHBOARD-SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Conversational guidance, Markdown briefs and agendas, shell commands, and JSON configuration updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update Google Calendar events through gog and write local meeting notes or schedule exports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
