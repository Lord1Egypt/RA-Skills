## Description: <br>
Monitor product-level and category-level price gaps, promo shifts, and visible trend signals using browser-collected marketplace data or user-provided price snapshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leooooooow](https://clawhub.ai/user/leooooooow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketplace sellers and pricing operators use this skill to compare visible ecommerce prices, normalize product or category snapshots, and decide whether to watch, react, or gather more data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Logged-in marketplace browsing can expose account areas beyond visible price research. <br>
Mitigation: Prefer guest or private browsing; if login is needed, restrict work to marketplace search and product pages and avoid orders, account settings, saved addresses, payment methods, carts, checkout, and seller or admin areas. <br>
Risk: Visible marketplace snapshots can be incomplete, stale, or mistaken for confirmed price trends. <br>
Mitigation: Label evidence strength, record timestamps and coverage, normalize price data, and avoid trend claims unless multiple time-separated observations support them. <br>


## Reference(s): <br>
- [Price Gap Monitor on ClawHub](https://clawhub.ai/leooooooow/price-gap-monitor) <br>
- [Output template](references/output-template.md) <br>
- [Pricing data collection guide](references/pricing-data-guide.md) <br>
- [Platform comparison reference](references/platform-comparison-guide.md) <br>
- [Quality checklist](assets/quality-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown analysis with tables, evidence labels, risk notes, and recommended actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use browser-collected marketplace snapshots or user-provided price data; outputs should identify collection method, timestamps, normalization notes, and evidence strength.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
