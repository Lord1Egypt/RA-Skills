## Description:

Helps agents query Shopee Account Health data for authorized stores through LinkFox, covering shop performance, metric source details, penalty points, punishments, listings with issues, and late orders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, operators, and support agents use this skill to inspect Shopee store health, diagnose account-health metric failures, and prioritize late orders, listing issues, penalty points, and punishment history for authorized shops.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles LinkFox API keys, Shopee account-health data, phone/SMS login flows, and billing or unpaid order flows.

Mitigation: Install only when the publisher is trusted for this data, avoid sharing OTPs or API keys in logs, and rotate any exposed key.

Risk: Custom gateway environment variables can redirect requests to endpoints outside the default LinkFox service.

Mitigation: Use custom gateway variables only for endpoints you control and verify before sending store identifiers or credentials.

Risk: Saved LinkFox response files may contain sensitive store, order, listing, or account-health data.

Mitigation: Review saved JSON files before sharing them and keep the linkfox session data directory under appropriate access controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-shopee-store-account-health)
- [Shopee Account Health get_shop_performance](https://open.shopee.com/documents/v2/v2.account_health.get_shop_performance?module=103&type=1)
- [API reference](references/api.md)
- [Onboarding guide](references/onboarding.md)
- [get_shop_performance API guide](references/apis/get-shop-performance.md)
- [get_metric_source_detail API guide](references/apis/get-metric-source-detail.md)
- [get_penalty_point_history API guide](references/apis/get-penalty-point-history.md)
- [get_punishment_history API guide](references/apis/get-punishment-history.md)
- [get_listings_with_issues API guide](references/apis/get-listings-with-issues.md)
- [get_late_orders API guide](references/apis/get-late-orders.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses or saved JSON response files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include Shopee store health, order, listing, penalty, and punishment data; large or full responses can be saved under a linkfox session data directory.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
