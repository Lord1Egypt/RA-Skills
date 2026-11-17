## Description:

Turns raw US meeting notes into a decision log and an owned action list with due dates, left as a draft for the organizer to send.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US project managers, chiefs of staff, and team leads use the skill to turn recurring internal meeting notes into dated decisions, owned action items, open questions, and an unsent follow-up draft.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Meeting notes may include sensitive personal or employment details, and generated drafts may be shared too broadly.

Mitigation: Use trusted input, remove sensitive details, save to a fresh output folder, and have the organizer review each draft before sharing.

Risk: The documented Markdown quickstart may not match the script's CSV input, and template placeholders may not be replaced as expected.

Mitigation: Confirm the accepted input format and inspect generated files for missing or incorrect fields before using them.

Risk: The optional Windows application is not needed for the documented workflow and has a separate trust decision.

Mitigation: Use the documented Python workflow unless the Windows application has been independently reviewed and trusted.

## Reference(s):

- [US rules for meeting records and follow-ups](artifact/references/meeting-record-rules.md)
- [Meeting Notes to Actions on ClawHub](https://clawhub.ai/rapidworker1/skills/meeting-notes-to-actions)
- [Publisher profile](https://clawhub.ai/user/rapidworker1)
- [Publisher homepage](https://github.com/rapidworker1)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [A decision log, action list, open items, needs-dates list, and follow-up message draft in Markdown.]

**Output Parameters:** [One meeting per request; actions include an owner role, due date, and definition of done when available.]

**Other Properties Related to Output:** [Drafts only; the organizer reviews and sends them. The output is not a payroll or timekeeping record.]

## Skill Version(s):

1.0.6 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
