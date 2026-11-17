## Description:

Book same-day psychiatric and mental health telehealth appointments through conversation, covering ADHD, anxiety, depression, insomnia, OCD, PTSD, and narcolepsy across supported U.S. states.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gljirain](https://clawhub.ai/user/gljirain)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to find and book virtual psychiatric or psychiatric NP appointments for supported mental health concerns, including insurance or cash-pay options. Agents use it to collect booking details, search provider availability, and submit appointment requests through the booking API.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The skill handles highly sensitive mental health, contact, date of birth, and insurance information.

Mitigation: Ask for explicit consent before sending booking details, collect only fields required for the selected appointment, and avoid storing patient information.

Risk: Booking payloads passed as command arguments may expose patient details in shell history, logs, or process listings.

Mitigation: Prefer stdin, temporary redacted channels, or another mechanism that avoids placing sensitive booking data directly in command arguments.

Risk: The API destination can be changed through configuration, which could send sensitive information to an unintended service.

Mitigation: Lock the booking API destination to the intended HTTPS host or require explicit review before allowing an override.

Risk: Scheduled appointments are not appropriate for crisis or immediate-danger situations.

Mitigation: Redirect crisis language to emergency or crisis resources instead of proceeding with booking.

## Reference(s):

- [Klarity Booking API Reference](artifact/references/api-reference.md)
- [Klarity Booking API](https://rx.helloklarity.com)
- [ClawHub Skill Page](https://clawhub.ai/gljirain/skills/mental-health-booking)
- [Publisher Profile](https://clawhub.ai/user/gljirain)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, guidance]

**Output Format:** [Conversational Markdown with shell command invocations and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include provider availability summaries, appointment booking confirmations, validation errors, and crisis redirection guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
