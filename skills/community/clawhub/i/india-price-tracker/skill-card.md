## Description:

Track and compare product prices across popular Indian stores (Amazon India, Flipkart, Reliance Digital, Croma, Vijay Sales, Tata CLiQ, and more), compute effective prices after offers/cashback, detect arbitrage opportunities, and monitor price history with alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anugotta](https://clawhub.ai/user/anugotta)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ecommerce analysts use this skill to compare India-focused store listings, estimate effective prices after discounts, cashback, and shipping, monitor price history, and prepare threshold alerts before implementing compliant live adapters.

### Deployment Geography for Use:

India

## Known Risks and Mitigations:

Risk: Generated mock prices may be mistaken for real market data.

Mitigation: Treat outputs as decision support only; validate compliant live adapters and manually verify high-value opportunities before purchase, resale, or arbitrage decisions.

Risk: Live store integrations can run into platform terms, rate limits, or regional legal restrictions.

Mitigation: Review each store's terms of service, use approved access methods, and complete legal or compliance review before enabling live automation.

Risk: Bulk monitoring can write alerts to a caller-provided file path.

Mitigation: Use explicit reviewed output paths and avoid pointing output at sensitive or unrelated files.

Risk: Incorrect SKU matching, availability, discount, cashback, shipping, or fee assumptions can create misleading arbitrage signals.

Mitigation: Compare exact variants only, flag uncertain matches for manual review, and document fee and rounding assumptions before relying on alerts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/anugotta/skills/india-price-tracker)
- [Clawdis Homepage](https://clawhub.ai/Michael-laffin/price-tracker)
- [Setup Guide](setup.md)
- [Validation Checklist](validation-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text reports with local Python command examples and optional alert files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default scripts use mock data; bulk monitoring can write alerts to a user-provided output path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
