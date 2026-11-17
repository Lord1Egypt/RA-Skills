## Description:

Buy AI services, crypto data, and digital goods on Pactum marketplace. Supports credit card, Alipay, WeChat Pay, and USDC payments. Register with email, search items, place orders, track delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fredm45](https://clawhub.ai/user/fredm45)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to browse Pactum marketplace listings, register with email verification, place free or paid orders, track delivery, and manage post-delivery actions such as retries, messages, disputes, and file downloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles powerful Pactum API keys and JWTs, and the security evidence warns that credentials may be exposed unsafely.

Mitigation: Do not share credentials through chat, Telegram, logs, or transcripts; store API keys and tokens only in a secure secret manager and rotate them if exposure is suspected.

Risk: Marketplace actions can spend funds, top up credit, deposit USDC escrow, release payment, or open disputes.

Mitigation: Require explicit user confirmation before purchases, credit top-ups, escrow deposits, payment release, disputes, or retries that could affect funds or orders.

Risk: Physical-item flows may submit shipping-address details.

Mitigation: Collect shipping information only when the selected item requires it, confirm the destination with the user, and avoid retaining address data after the transaction workflow is complete.

## Reference(s):

- [Pactum Marketplace Skill Page](https://clawhub.ai/fredm45/skills/pactum)
- [Pactum](https://www.pactum.cc)
- [Pactum Gateway API](https://api.pactum.cc)
- [Pactum Orders Web UI](https://www.pactum.cc/orders)
- [Pactum Telegram Bot](https://t.me/Pactum_Market_Bot)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python requests examples and REST workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to make marketplace API calls, handle credentials, submit payments, provide shipping details, and download delivered files.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
