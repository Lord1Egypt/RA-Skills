## Description: <br>
Meeting Scheduler Pro helps an agent schedule meetings, manage availability, prepare briefs and agendas, and draft follow-ups using Google Calendar and optional Gmail, web search, and local meeting-note context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nollio](https://clawhub.ai/user/nollio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and teams use this skill to coordinate meetings through an agent: finding open slots, booking calendar events, generating meeting prep and agendas, and capturing follow-up actions after calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Calendar, Gmail, web-search, and local note data can contain sensitive business or personal information. <br>
Mitigation: Install only with Google permissions you accept, review config/settings.json after setup, and disable email context or web search when those data flows are not appropriate. <br>
Risk: Generated meeting notes, agendas, follow-ups, and dashboard history may persist sensitive meeting context locally. <br>
Mitigation: Treat the notes directory and dashboard history as sensitive records; secure, review, prune, or delete them according to your retention needs. <br>
Risk: AI-generated prep briefs, agendas, and follow-up drafts may be incomplete or inaccurate. <br>
Mitigation: Review generated meeting content before relying on it, sharing it with attendees, or sending follow-up email. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nollio/normieclaw-meeting-scheduler-pro) <br>
- [Publisher profile](https://clawhub.ai/user/nollio) <br>
- [OpenClaw](https://openclaw.com) <br>
- [NormieClaw](https://normieclaw.ai) <br>
- [README.md](README.md) <br>
- [SECURITY.md](SECURITY.md) <br>
- [Dashboard specification](dashboard-kit/DASHBOARD-SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Conversational text and Markdown, with shell commands and JSON configuration updates when setup or calendar workflows require them.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create Google Calendar events through gog, local meeting notes, prep briefs, agendas, follow-up drafts, and dashboard metrics when the user authorizes those actions.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
