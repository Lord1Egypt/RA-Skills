## Description: <br>
商品比价 helps agents compare product prices across major e-commerce platforms by collecting prices, parsing promotions, normalizing final costs, and producing purchase recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhang3feng](https://clawhub.ai/user/zhang3feng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and procurement teams use this skill to compare the same product across platforms such as JD, Tmall, Taobao, Pinduoduo, and Suning. It is intended for price comparison reports that include current price, historical low, promotion details, delivery timing, and purchase guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated browsing of e-commerce sites can expose shopping-session data such as addresses, order history, payment methods, or coupons. <br>
Mitigation: Prefer unauthenticated browsing or a dedicated test account, and avoid using real shopping sessions for price checks. <br>
Risk: Target platforms may restrict scraping or automated access. <br>
Mitigation: Confirm that automated browsing is allowed for the target platform and use case before running the skill. <br>
Risk: Prices, discounts, inventory, and coupons can change between report generation and checkout. <br>
Mitigation: Treat the report as decision support, verify the final checkout price manually, and act promptly when price freshness matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhang3feng/product-price-compare) <br>
- [Platform DOM reference](references/platform-dom.md) <br>
- [Promotion rules reference](references/promotion-rules.md) <br>
- [Price normalization reference](references/normalization.md) <br>
- [Usage examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown price comparison report with tables and concise recommendation text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include platform names, current prices, historical lows, promotion details, delivery timing, and purchase recommendation notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
