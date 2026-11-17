## Description:

Connect to a real human psychologist through a REST API, with a free first message and paid USDC follow-up messages in English or Spanish.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaugoustis](https://clawhub.ai/user/aaugoustis)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to send a concise wellbeing or psychology-related message to a human respondent, retrieve replies later, and handle paid follow-up messages when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messages may include sensitive mental-health content and are sent to an external API, a human recipient, and Telegram.

Mitigation: Warn users before submission, avoid names, contact details, diagnoses, crisis information, or other sensitive identifiers, and obtain explicit consent for external handling.

Risk: Follow-up messages can require USDC payments that may be irreversible.

Mitigation: Independently verify the Base network, USDC token contract, amount, and recipient address returned by the API before transferring funds.

Risk: The service depends on a human response that can take from 5 minutes to 10 hours.

Mitigation: Set expectations before sending a message and provide the session ID so the user can check for replies later.

## Reference(s):

- [API documentation](https://ai-psychologist-api.replit.app/docs)
- [ClawHub skill page](https://clawhub.ai/aaugoustis/skills/human-psychologist)

## Skill Output:

**Output Type(s):** [Text, API calls, Guidance]

**Output Format:** [Markdown or plain text with JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Messages are limited to 300 words; human replies may take 5 minutes to 10 hours; follow-up messages may require USDC payment verification.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
