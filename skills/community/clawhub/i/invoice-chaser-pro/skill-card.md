## Description: <br>
Generate escalating payment reminder emails that match days-past-due. Four stages: friendly, firm, urgent, final notice. Supports contractor, professional, and general business verticals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[josh4hire](https://clawhub.ai/user/josh4hire) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Small-business operators, contractors, and professional service providers use this skill to draft concise payment reminder emails for overdue invoices, including staged escalation from friendly reminders through final notices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill drafts payment reminders that may affect client relationships or collections posture. <br>
Mitigation: Review every generated email before sending and confirm that the tone, facts, dates, and requested payment terms match the business context. <br>
Risk: The skill requests local file read and write access without a clearly scoped file workflow. <br>
Mitigation: Grant file access only for specific invoice files or draft locations, and avoid persisting sensitive billing details unless necessary. <br>


## Reference(s): <br>
- [Invoice Chaser Pro on ClawHub](https://clawhub.ai/josh4hire/invoice-chaser-pro) <br>
- [Publisher profile](https://clawhub.ai/user/josh4hire) <br>
- [Project homepage](https://gaffneyits.com/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown email draft with stage, vertical, days overdue, subject, and body sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can generate a single reminder or a four-stage sequence; each email is intended to stay under 150 words.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
