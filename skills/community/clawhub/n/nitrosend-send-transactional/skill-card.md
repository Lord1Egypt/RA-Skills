## Description:

Send transactional emails or SMS for app-triggered communications: receipts, password resets, OTPs, order confirmations, shipping notifications, system alerts. Single recipient, immediate delivery, no campaign or approval needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nitrosend](https://clawhub.ai/user/nitrosend)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to send immediate, single-recipient transactional email or SMS and to integrate app-triggered messages for authentication, receipts, orders, shipping, and service updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Transactional messages can contain recipient details and sensitive content such as verification codes; opens and clicks are tracked.

Mitigation: Use the offered dry run, verify the recipient and content before live delivery, account for engagement tracking, and keep API keys in backend secret storage.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/nitrosend/skills/nitrosend-send-transactional)
- [Nitrosend transactional messages endpoint](https://api.nitrosend.com/v1/my/messages)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration]

**Output Format:** [Markdown guidance with REST/JSON request examples and JavaScript SDK code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include personalized message content and transactional email or SMS integration instructions.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
