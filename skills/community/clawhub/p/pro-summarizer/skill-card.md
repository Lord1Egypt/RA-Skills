## Description:

Produces a concise Chinese summary, three English SEO keywords, and a follow-up insight after a pay-per-use billing check.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hxo-resistor](https://clawhub.ai/user/hxo-resistor)

### License/Terms of Use:

MIT-0

## Use Case:

People who want a paid summary of supplied text with SEO keywords and a brief reflection can use this skill after confirming the charge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests a charge before summarizing, without an explicit consent step.

Mitigation: Use only if you intend to pay per invocation; require clear consent before enabling charges.

Risk: The stated price and per-call charge differ, and refund terms are unclear.

Mitigation: Confirm the actual charge, currency, and refund or reversal process with the publisher before use.

Risk: Billing sends a user identifier to an external service using configured payment credentials.

Mitigation: Confirm who controls the billing credentials and whether sharing the user identifier is acceptable.

Risk: The skill includes unrelated image-prompt instructions that may cause inconsistent responses.

Mitigation: Review the outputs and ask the publisher to remove the unrelated instructions.

## Reference(s):

- [Pro Summarizer on ClawHub](https://clawhub.ai/hxo-resistor/skills/pro-summarizer)
- [SkillPay billing service](https://skillpay.me)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [JSON in a Markdown code block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese summary of up to 200 characters, three English SEO keywords, and a Chinese insight of up to 100 characters; a payment URL may be returned instead if billing fails.]

## Skill Version(s):

1.0.4 (source: skill frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
