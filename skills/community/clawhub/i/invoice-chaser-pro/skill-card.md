## Description:

Generate escalating payment reminder emails that match days-past-due, with friendly, firm, urgent, and final notice stages for contractor, professional, and general business contexts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[josh4hire](https://clawhub.ai/user/josh4hire)

### License/Terms of Use:

MIT-0

## Use Case:

External business users, contractors, and accounts-receivable teams use this skill to draft concise payment reminder emails and escalation sequences from invoice details they provide.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill works with invoice and client payment details, which can be sensitive business information.

Mitigation: Invoke it explicitly in finance workflows and grant file access only to user-selected invoice or template files.

Risk: Collections language can be mistaken for legal advice or overstate available remedies.

Mitigation: Keep outputs to reminder emails, require human review before sending, and consult a collections attorney for legal remedies.

## Reference(s):

- [OpenClaw homepage](https://gaffneyits.com/openclaw)
- [ClawHub skill page](https://clawhub.ai/josh4hire/skills/invoice-chaser-pro)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown email draft with stage, vertical, days-overdue, subject, and body sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate a single reminder or a four-stage sequence; email bodies are intended to stay under 150 words.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
