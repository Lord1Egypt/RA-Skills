## Description:

Queries a Shopify store's sales, profitability, customer, product, and marketing data through Ned's API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matt998759](https://clawhub.ai/user/matt998759)

### License/Terms of Use:


## Use Case:

External Shopify merchants and their agents use this skill to query Ned for store profitability, product performance, customer segments, churn risk, and marketing efficiency using a Ned API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a Ned API key to retrieve sensitive business, customer, product-margin, churn-risk, and advertising-performance analytics.

Mitigation: Use a scoped or revocable API key when available, avoid exposing the key in logs or chats, and require explicit confirmation for sensitive analytics queries.

Risk: Broad natural-language prompts may cause an agent to retrieve more store data than the user intended.

Mitigation: Confirm the requested endpoint, period, and customer-level scope before running customer, churn, product-margin, or ad-performance queries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/matt998759/skills/ned-analytics)
- [Ned website](https://meetned.com)
- [Ned API base](https://api.meetned.com/api/v1)

## Skill Output:

**Output Type(s):** [Text, Shell commands, API calls, JSON, Guidance]

**Output Format:** [Markdown or plain text with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NED_API_KEY and queries Ned API endpoints subject to rate limits and plan credits.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
