## Description:

Drills into all Ozon Russia products for a numeric seller ID and returns per-SKU sales, revenue, price, rating, stock, turnover, lost-profit, filtering, sorting, and currency-conversion data for store audits and competitor benchmarking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and e-commerce operators use this skill to inspect the product table under a specific Ozon seller ID, identify seller bestsellers, review inventory and lost-sales signals, and compare competitor store structures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags account onboarding, SMS-code login, billing and paid-credit purchase flows, credential handling, endpoint overrides, local response retention, and automatic feedback reporting as behaviors requiring review.

Mitigation: Install and run the skill only after reviewing the publisher, endpoint configuration, and security guidance; do not enter SMS codes, payment choices, or API keys unless the LinkFox publisher and endpoints are trusted.

Risk: The skill consumes paid compute credits and the artifact states one seller-products call costs compute units unless the returned list is empty.

Mitigation: Confirm the user wants to spend credits before calls, avoid automatic retries or exploratory paging, and narrow filters before additional paid requests.

Risk: The scripts read LinkFox API keys from environment variables and onboarding material suggests persistent shell-profile configuration.

Mitigation: Prefer temporary environment variables or a secure secret manager, avoid writing API keys into shell startup files, and rotate exposed keys.

Risk: Full API responses are retained locally in a linkfox session data directory and cached for 24 hours.

Mitigation: Treat saved response files as potentially sensitive business data, store them only in approved workspaces, and delete cached or session data when no longer needed.

Risk: Feedback may be reported to a separate LinkFox feedback endpoint.

Mitigation: Avoid including confidential seller data, credentials, payment details, or private user context in feedback content.

## Reference(s):

- [API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-mpstats-ozon-seller-products)
- [Publisher Profile](https://clawhub.ai/user/linkfox-ai)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell commands, and JSON API responses or saved response-file summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script saves full API responses under a local linkfox session data directory and may print either full JSON or a compact summary depending on response size.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
