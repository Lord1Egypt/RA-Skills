## Description: <br>
Generate and send a daily briefing to your owner covering today's meetings, urgent emails, open tasks, and anything that needs attention. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netanel-abergel](https://clawhub.ai/user/netanel-abergel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, operators, and personal assistants use this skill to prepare and send a concise daily owner briefing from calendar events, unread email, open monday.com tasks, and items needing attention. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The briefing may expose meeting titles, email senders, subjects, and task names through the selected delivery channel. <br>
Mitigation: Use the skill only with an approved channel and recipient, and confirm that WhatsApp or email is appropriate for the organization's data. <br>
Risk: Incorrect account, board, token, recipient, or timezone settings can send incomplete or misdirected briefings. <br>
Mitigation: Before enabling cron, verify the Google account, monday.com board ID, token scope, OWNER_PHONE or email recipient, and timezone. <br>


## Reference(s): <br>
- [Owner Briefing on ClawHub](https://clawhub.ai/netanel-abergel/owner-briefing) <br>
- [monday.com API endpoint](https://api.monday.com/v2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with bash and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a concise briefing message and optional cron configuration.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
