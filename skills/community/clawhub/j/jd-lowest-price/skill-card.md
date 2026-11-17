## Description:

Queries JD.com self-operated products that are currently at historical low prices, with filters for keyword, maximum price, review rate, pagination, and sorting by recommendation, price, or discount depth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cn-shopping](https://clawhub.ai/user/cn-shopping)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers and shopping assistants use this skill to find JD.com self-operated products that are currently at historical low prices, then narrow results by brand, category, budget, review rate, and discount depth. It provides product information and purchase links, but does not buy products, show historical price curves, or create price alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shopping search terms are relayed through the publisher's Tencent Cloud proxy.

Mitigation: Install only if that proxy data flow is acceptable, and review publisher documentation for data handling, retention, and proxy behavior.

Risk: The skill includes a reusable fallback proxy token.

Mitigation: Use an environment-provided token, rotate the exposed token, and remove the hardcoded fallback secret before relying on the skill in managed environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cn-shopping/skills/jd-lowest-price)
- [Publisher profile](https://clawhub.ai/user/cn-shopping)
- [京东自营超级补贴](https://clawhub.ai/cn-shopping/jd-super-deals)
- [京东自营9.9包邮](https://clawhub.ai/cn-shopping/jd-99-baoyou)
- [购物比价助手](https://clawhub.ai/cn-shopping/best-price)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON string containing a human-readable summary and a JSON-encoded product list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Product results may include names, prices, discount percentages, shop and brand names, tags, image URLs, buy URLs, categories, recent order counts, review rates, and scores.]

## Skill Version(s):

1.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
