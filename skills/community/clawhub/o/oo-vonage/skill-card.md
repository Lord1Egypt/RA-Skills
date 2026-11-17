## Description:

Vonage (vonage.com). Use this skill for ANY Vonage request — reading, creating, and updating data. Whenever a task involves Vonage, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to check a connected Vonage account balance, retrieve SMS delivery records, and send SMS messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes unverified remote code, and startup synchronization may add or refresh other agent skills.

Mitigation: Review and install the CLI separately before use; disable startup skill synchronization if you do not want other agent skills added or refreshed.

Risk: Sending an SMS can incur a charge.

Mitigation: Confirm the recipient, message, and potential charge before sending.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Vonage SMS API documentation](https://developer.vonage.com/en/api/sms)

## Skill Output:

**Output Type(s):** [API Calls, JSON data, Text messages]

**Output Format:** [JSON action results and SMS text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads return account balance or SMS delivery data; sending submits a text or Unicode SMS.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
