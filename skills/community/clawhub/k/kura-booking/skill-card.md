## Description:

Helps an agent use e-pai-ke.com (E-Pai-Ke) to manage restaurant login, search, queue status checks, bookings, and reservation cancellations for restaurants such as Kura Sushi.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dabendan2](https://clawhub.ai/user/dabendan2)

### License/Terms of Use:

MIT-0

## Use Case:

External users with E-Pai-Ke accounts use this skill to check restaurant queue status and manage reservations. It is intended for agent-assisted booking workflows where the user confirms exact restaurant, time, party size, and cancellation details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use saved E-Pai-Ke login credentials.

Mitigation: Keep credentials out of plain notes where possible and avoid screenshots or logs during login.

Risk: Reservation booking or cancellation could proceed with the wrong details.

Mitigation: Require explicit confirmation of restaurant, date, time, party size, and cancellation target before the agent completes the action.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/dabendan2/skills/kura-booking)
- [E-Pai-Ke website](https://e-pai-ke.com/)
- [E-Pai-Ke reservation management](https://e-pai-ke.com/reservationA)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with inline JavaScript and shell-oriented automation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide browser or Playwright actions for booking, queue checks, login, and cancellation workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
