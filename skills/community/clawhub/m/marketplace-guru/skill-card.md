## Description: <br>
Marketplace Guru helps users find and compare marketplace products through disciplined purchase intake, multi-source market mapping, price and risk analysis, and decision-ready recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pe4atnik](https://clawhub.ai/user/pe4atnik) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to research, compare, choose, or verify marketplace and online-store purchases when delivery, current price, reviews, seller quality, alternatives, or purchase risk matter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional browser use may expose marketplace account context, saved sessions, or account-specific pricing. <br>
Mitigation: Use a dedicated browser profile without saved payment methods and keep login, cart, payment, seller messaging, and account changes under direct user control. <br>
Risk: Marketplace prices, stock, seller quality, discounts, and delivery estimates can change quickly or vary by region/account. <br>
Mitigation: Treat recommendations as product research, verify final price and delivery before checkout, and preserve the skill's audit trail of searched sources and unverified items. <br>


## Reference(s): <br>
- [Marketplace Guru on ClawHub](https://clawhub.ai/pe4atnik/marketplace-guru) <br>
- [Publisher profile](https://clawhub.ai/user/pe4atnik) <br>
- [Design notes](references/design-notes.md) <br>
- [Legacy marketplace scraper reference](references/legacy/marketplace-scraper/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, text] <br>
**Output Format:** [Markdown recommendation with source audit, market map, priced options, risk notes, and unverified follow-ups] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include product links, prices, delivery region, seller/source details, timestamps, and avoid/risky option labels when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
