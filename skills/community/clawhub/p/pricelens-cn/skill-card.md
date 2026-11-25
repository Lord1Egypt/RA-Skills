## Description:

Given a product category and budget, PriceLens produces a traceable landed-price range, compares channel trust and product trade-offs, and gives a quantified buy, wait, or switch recommendation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengjianli0721](https://clawhub.ai/user/fengjianli0721)

### License/Terms of Use:

MIT-0

## Use Case:

External consumers use PriceLens to compare documented product prices and sales channels, weigh three user-prioritized requirements, and decide whether to buy now, wait, or choose an alternative.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags a concern about potentially misleading assurances when handling sensitive ownership and financial data; the scan was partial because one reference could not be resolved.

Mitigation: Review the requested data before use, share only details needed for the comparison, omit identifying, contact, address, account, and payment information, and check reports for sensitive asset or valuation details before sharing.

## Reference(s):

- [Price Evidence Chain](artifact/references/price-evidence-chain.md)
- [Channel Matrix](artifact/references/channel-matrix.md)
- [Value Scoring](artifact/references/value-scoring.md)
- [Decision Report](artifact/references/decision-report.md)
- [ClawHub release page](https://clawhub.ai/fengjianli0721/skills/pricelens-cn)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown decision report with pricing tables, a trade-off matrix, and an evidence checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Six fixed sections; timestamped price evidence, review items, and a buy, wait, or switch verdict with a trigger condition.]

## Skill Version(s):

1.0.1 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
