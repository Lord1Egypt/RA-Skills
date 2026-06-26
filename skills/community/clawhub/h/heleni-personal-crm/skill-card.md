## Description: <br>
Personal CRM built on monday.com that tracks contacts, interactions, meetings, and topics, syncs daily from Calendar and email, and delivers pre-meeting briefings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netanel-abergel](https://clawhub.ai/user/netanel-abergel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees or personal CRM users use this skill to keep a monday.com contact board current from calendar and email context, prepare for meetings, and query relationship history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can repeatedly read calendar and CRM data and may expose private meeting notes through outbound briefings. <br>
Mitigation: Install only for the intended monday.com board, calendar, Gmail context, and WhatsApp destination; redact Notes by default. <br>
Risk: Automated CRM writes and WhatsApp sends may occur without enough scoping or approval controls. <br>
Mitigation: Use scoped managed authentication, verify the board and recipient, and require approval before CRM writes or outbound messages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/netanel-abergel/heleni-personal-crm) <br>
- [Google Calendar API events endpoint](https://www.googleapis.com/calendar/v3/calendars/netanelab%40monday.com/events?timeMin=${TODAY}T00:00:00Z&timeMax=${TOMORROW}T00:00:00Z&singleEvents=true&orderBy=startTime) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and operational instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include CRM updates, meeting briefing text, cron setup commands, and WhatsApp delivery guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
