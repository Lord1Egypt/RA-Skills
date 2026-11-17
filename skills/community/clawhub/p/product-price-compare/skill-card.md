## Description:

商品比价 compares products across major e-commerce platforms by collecting prices, parsing promotions, normalizing final prices, and producing purchase recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhang3feng](https://clawhub.ai/user/zhang3feng)

### License/Terms of Use:

MIT-0

## Use Case:

External users, procurement teams, and shopping researchers use this skill to compare the same product across e-commerce platforms, normalize discounts and shipping, and receive a concise price comparison report. It is intended for product selection, bulk purchase checks, sale-period comparisons, and advisory purchase recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automate visits to third-party shopping sites and includes anti-bot evasion guidance.

Mitigation: Use only where site terms, consent, and rate limits permit; avoid logged-in shopping sessions or sensitive purchasing accounts until the release defines compliant automation behavior.

Risk: The scanner describes the release as incomplete, so price, discount, and history outputs may be unreliable.

Mitigation: Treat results as advisory and verify prices, coupons, stock, shipping, and historical lows on the platform checkout or other trusted sources before purchasing.

Risk: Report storage and sensitive account handling are not defined in the evidence.

Mitigation: Run in an isolated environment, avoid collecting credentials or account-specific coupons, and define retention and cleanup behavior before deployment.

## Reference(s):

- [Platform DOM Reference](artifact/references/platform-dom.md)
- [Promotion Rules](artifact/references/promotion-rules.md)
- [Price Normalization Algorithm](artifact/references/normalization.md)
- [Usage Examples](artifact/references/examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown comparison reports with tables and purchase recommendations; helper scripts may emit JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include platform, current price, historical low, promotion details, delivery timing, normalized final price, and recommendation status.]

## Skill Version(s):

1.0.0 (source: server release metadata and README changelog, released 2026-03-29)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
