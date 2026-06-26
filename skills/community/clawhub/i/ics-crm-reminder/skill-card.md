## Description: <br>
Generates ICS calendar files with structured CRM data for B2B sales follow-ups, including customer details, deal status, priority, and next steps for Apple Calendar, Google Calendar, and Outlook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kopfkinok3](https://clawhub.ai/user/kopfkinok3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales teams and business users use this skill to create calendar reminders for customer calls, follow-ups, and sales meetings from structured or freeform CRM details. The agent collects required company, date, and time fields, then generates an importable calendar file with the follow-up context in the event description. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated calendar files can contain CRM and personal contact details that may sync to calendar providers, shared devices, backups, or forwarded calendar invites. <br>
Mitigation: Keep confidential notes, sensitive budget terms, and internal sales status out of reminders unless the destination calendar and sharing settings are appropriate for that data. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/visales/ics-crm-reminder) <br>
- [ClawHub skill page](https://clawhub.ai/kopfkinok3/ics-crm-reminder) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Markdown, Configuration instructions] <br>
**Output Format:** [ICS calendar file plus concise Markdown summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces one .ics file per reminder and may include customer, contact, deal, budget, next-step, and note fields in the calendar event description.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
