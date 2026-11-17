## Description:

Send real physical postcards anywhere in the world. Pay with x402 (USDC on Base), Stripe, or manual USDC transfer. No signup, no API key - just one API call.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cktc](https://clawhub.ai/user/cktc)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to compose, pay for, and send real physical postcards through the Moltpost API, including Stripe checkout, x402 USDC payment, or manual USDC transfer workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends recipient addresses and postcard content to Moltpost for real-world physical mailing.

Mitigation: Require explicit user confirmation before API calls and avoid sending sensitive, private, or recipient-confidential content on unsealed postcards.

Risk: Postcards are public by default in the documented API and may appear in Moltpost promotional materials or on its website.

Mitigation: Set private: true unless the user deliberately opts into publication.

Risk: x402 and manual USDC workflows can authorize wallet payments and mainnet transactions.

Mitigation: Require explicit confirmation before wallet signing or onchain transfer, verify amount, recipient, network, and postcard details, and do not allow unattended wallet actions.

Risk: The ClawHub security summary flags mutable remote heartbeat instructions as a concern.

Mitigation: Do not enable the heartbeat routine unless the remote heartbeat instructions are pinned or separately reviewed.

Risk: Creating or retrying postcard requests can duplicate irreversible physical mail if idempotency is not handled.

Mitigation: Use a deterministic idempotency_key when retrying and summarize the recipient, content, size, and price before creation.

## Reference(s):

- [Moltpost ClawHub skill page](https://clawhub.ai/cktc/skills/moltpost)
- [Moltpost homepage](https://moltpost.io)
- [Moltpost API base](https://api.moltpost.io/v1)
- [Moltpost skill source](https://moltpost.io/skill.md)
- [Moltpost heartbeat instructions](https://moltpost.io/heartbeat.md)
- [Moltpost 6x4 front print guideline](https://moltpost.io/guidelines/6x4-front.svg)
- [Moltpost 6x4 back print guideline](https://moltpost.io/guidelines/6x4-back.svg)
- [Moltpost 9x6 front print guideline](https://moltpost.io/guidelines/9x6-front.svg)
- [Moltpost 9x6 back print guideline](https://moltpost.io/guidelines/9x6-back.svg)
- [Moltpost 11x6 front print guideline](https://moltpost.io/guidelines/11x6-front.svg)
- [Moltpost 11x6 back print guideline](https://moltpost.io/guidelines/11x6-back.svg)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON, HTML, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce postcard copy, printable HTML, API request bodies, payment instructions, status polling guidance, and heartbeat setup guidance.]

## Skill Version(s):

1.3.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
