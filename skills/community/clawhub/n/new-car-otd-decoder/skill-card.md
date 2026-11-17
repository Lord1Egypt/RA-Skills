## Description:

Use when reviewing a new-car purchase quote, lease deal, or 'out-the-door' price. Audits OTD line items (doc fees vs state caps, taxed rebates, dealer add-on padding), decodes lease money factor into real APR, and compares financing against a pre-approved loan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

External car buyers use the skill to audit itemized new-car purchase and lease quotes, check fee and tax treatment, compare payment and financing figures, and prepare a negotiation response.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Quote details can contain personal identifiers.

Mitigation: Share only the quote details needed for analysis and omit personal identifiers.

Risk: State fee and tax rules or lender figures may have changed or may be entered incorrectly.

Mitigation: Verify current state rules and lender figures before relying on classifications or calculated totals.

Risk: A negotiation draft may need adjustment before it is sent.

Mitigation: Review negotiation drafts before sending them.

## Reference(s):

- [State Rules — Doc-Fee Caps, Rebate Taxation, Trade-In Taxation](references/state-rules.md)
- [Dealer Add-On Catalog — Fair Values vs Charged Prices](references/addon-catalog.md)
- [Negotiation Playbook — Getting an Honest OTD by Email](references/negotiation-playbook.md)
- [ClawHub release](https://clawhub.ai/voronindenis5/skills/new-car-otd-decoder)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown quote audit with verdicts, totals, payment checks, and negotiation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calculations and classifications depend on the quote details and current state and lender rules.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
