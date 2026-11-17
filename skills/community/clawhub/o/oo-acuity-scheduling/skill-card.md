## Description:

Use Acuity Scheduling to read, create, update, and delete scheduling data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People managing appointments use this skill to retrieve account, calendar, intake form, appointment, and availability information, or to make appointment changes in Acuity Scheduling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions can run downloaded software whose release has not been verified.

Mitigation: Install a verified oo CLI release yourself, require permission before additional software installation, and check whether it adds or updates other agent skills.

Risk: Connecting Acuity gives OOMOL access to scheduling data, and appointment changes can affect bookings.

Mitigation: Review the connected account access and keep the documented approval checks for appointment changes and cancellations.

## Reference(s):

- [Acuity Scheduling API documentation](https://developers.acuityscheduling.com/)
- [Acuity Scheduling](https://acuityscheduling.com/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [Acuity Scheduling skill release on ClawHub](https://clawhub.ai/oomol/skills/oo-acuity-scheduling)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON action results and user-facing text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Appointment changes require user confirmation; cancellations require explicit approval.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
