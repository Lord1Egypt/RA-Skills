## Description:

Book restaurant tables on OpenTable through a browser agent, including flows where time slots and terms checkboxes are not exposed in the page snapshot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eeshita-pande](https://clawhub.ai/user/eeshita-pande)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to reserve restaurant tables on OpenTable with a logged-in browser session. It is intended for OpenTable bookings where the user already has an account session and saved payment card.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can act inside a logged-in OpenTable account and complete reservations using a saved card.

Mitigation: Require explicit user confirmation of restaurant, date, time, party size, and booking type before completing the reservation.

Risk: The skill can accept OpenTable terms automatically during booking.

Mitigation: Surface the terms step to the user and proceed only when the user agrees to continue.

Risk: Booking pages may expose personal details or payment-adjacent information from the user's OpenTable account.

Mitigation: Limit reporting to reservation details and card last four digits; do not expose full payment credentials or unnecessary account details.

## Reference(s):

- [Browser Snippet Reference](browser-snippets.md)
- [ClawHub Skill Page](https://clawhub.ai/eeshita-pande/skills/opentable-booking)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown instructions with JavaScript snippets and final text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires browser access, an authenticated OpenTable session, and a saved card on file.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
