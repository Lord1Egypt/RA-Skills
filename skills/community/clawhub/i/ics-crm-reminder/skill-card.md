## Description:

Generates importable ICS calendar reminders that embed structured CRM details for B2B sales follow-ups across Apple Calendar, Google Calendar, and Outlook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kopfkinok3](https://clawhub.ai/user/kopfkinok3)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and customer-facing teams use this skill to turn CRM follow-up details into calendar reminders with customer, deal, priority, and next-step information. It is useful when an agent needs to collect required reminder fields, run the generator, and return a concise file summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calendar reminders may contain contact, deal, budget, and note details that sync to calendar services.

Mitigation: Generate files only from trusted CRM text and review each ICS file before importing it into a calendar account.

Risk: User-selected output paths can place generated calendar files outside the intended working area.

Mitigation: Write generated ICS files to a dedicated workspace folder and confirm the destination path before import or sharing.

Risk: ICS escaping or formatting issues could affect how calendar applications display CRM details.

Mitigation: Open and inspect the generated reminder in the target calendar application before relying on it for follow-up workflow.

## Reference(s):

- [Project homepage](https://github.com/visales/ics-crm-reminder)
- [ClawHub skill page](https://clawhub.ai/kopfkinok3/skills/ics-crm-reminder)
- [Publisher profile](https://clawhub.ai/user/kopfkinok3)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Markdown, Guidance]

**Output Format:** [ICS calendar files with a concise Markdown summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reminders may include customer contact details, deal status, budget, notes, priority, duration, and alarm timing.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
