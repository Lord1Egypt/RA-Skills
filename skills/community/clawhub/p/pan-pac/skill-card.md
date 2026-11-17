## Description:

Pan Pac helps agents handle Pan Pacific Travel email, calendar, and booking workflows by extracting booking details and routing Lynx and Outlook work to the appropriate skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fredguile](https://clawhub.ai/user/fredguile)

### License/Terms of Use:

MIT-0

## Use Case:

Travel operations staff and their agents use this skill to interpret Pan Pacific Travel communications, extract booking details, and coordinate follow-up through dedicated email/calendar and Lynx booking skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delegated Outlook and Lynx workflows may expose email, calendar, attachment, OAuth token, or booking-record data through downstream skills.

Mitigation: Install only for intended Pan Pacific Travel workflows and review the outlook-entra and lynx-skill permissions before use.

Risk: Extracted booking details such as dates, passengers, reservation status, modifications, and cancellations may be acted on incorrectly if not checked.

Mitigation: Review extracted details and downstream booking results before customer, provider, or itinerary actions.

## Reference(s):

- [Pan Pac ClawHub skill page](https://clawhub.ai/fredguile/skills/pan-pac)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Markdown and natural-language responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May delegate email/calendar and booking operations to outlook-entra and lynx-skill when those skills are available.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter version 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
