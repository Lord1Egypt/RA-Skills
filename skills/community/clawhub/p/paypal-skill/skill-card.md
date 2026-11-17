## Description:

Registers a PayPal skill for organizing public financial-service pages, product descriptions, rate rules, service boundaries, and help information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mike47512](https://clawhub.ai/user/mike47512)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to summarize public PayPal product pages, fee rules, help content, security notices, and service boundaries. It is intended for public-information organization only, not account access, transaction execution, financial advice, or private data processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public PayPal rates, product terms, regions, and help content may change over time.

Mitigation: Check the current public PayPal page, capture the page date, and state the applicable region in outputs.

Risk: Summaries of financial-service pages could be mistaken for investment, lending, tax, or account advice.

Mitigation: Frame outputs as public information summaries and avoid recommendations, account instructions, or transaction decisions.

Risk: Using the skill with private PayPal account or payment data would exceed the documented boundary.

Mitigation: Use only public pages and do not provide logged-in sessions, balances, identity documents, payment cards, or private transaction details.

## Reference(s):

- [PayPal Official Site](https://www.paypal.com/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summaries, tables, and checklists based on public PayPal pages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should identify page date and applicable region when summarizing time-sensitive financial information.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
