## Description:

Create and fund bitcoin gifts over the Lightning Network with the lightning.gifts API — sign in, mint a gift, pay its BOLT11 invoice, hand off a claim link, reclaim an expired one. Use when sending someone bitcoin as a gift, or when a task mentions lightning.gifts, gifting sats, or a gift's funding invoice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wahidmy](https://clawhub.ai/user/wahidmy)

### License/Terms of Use:

Blue Oak Model License 1.0.0

## Use Case:

People sending bitcoin gifts and developers automating the giver flow use this skill to create and fund Lightning gifts, deliver claim links, and reclaim eligible expired gifts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Creating a gift requires paying an external Lightning invoice, including the service fee.

Mitigation: Check payment capability and confirm the amount, fee, and deployment limit before paying; verify settlement before continuing.

Risk: A claim link contains a one-time token that grants access to the gift.

Mitigation: Share the complete link only with the recipient over a trusted channel; do not log or post it publicly.

Risk: A per-user API key acts as its owner and has no scopes or expiry.

Mitigation: Store it as a secret and send it only in the Authorization header, never in a URL, log, or committed example.

## Reference(s):

- [Lightning Gifts API reference](https://lightning.gifts/api-docs.md)
- [Lightning Gifts service](https://lightning.gifts)
- [Lightning Gifts agent contract](https://lightning.gifts/llms.txt)
- [Endpoints](references/endpoints.md)
- [Pitfalls](references/pitfalls.md)
- [ClawHub release page](https://clawhub.ai/wahidmy/skills/lightning-gifts)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, Guidance]

**Output Format:** [Markdown with JSON request examples and inline shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Step-by-step giver workflow, operational checks, and error-handling guidance]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
