## Description:

This skill helps agents browse Kalodata TikTok Shop leaderboards and fetch detailed metrics for a selected TikTok shop by shopId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External commerce users and analysts use this skill to discover high-performing TikTok Shop stores by market and date range, then inspect a selected store's GMV, sales volume, product count, revenue-channel split, and creator activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: LinkFox receives TikTok shop lookup queries and related parameters.

Mitigation: Use the skill only for queries the user is comfortable sending to LinkFox, and avoid custom LINKFOX_* endpoint overrides unless the endpoint is trusted.

Risk: The onboarding flow can handle account recovery, SMS-code login, billing-plan selection, and payment-order creation.

Mitigation: Do not provide SMS codes or create payment orders unless the user explicitly wants to resolve authentication or billing.

Risk: API keys and response data may be persisted through shell-profile configuration, local output files, or cache files.

Mitigation: Prefer a secure secret store or session-scoped environment variable for API keys, avoid committing generated files, and clear local outputs when they are no longer needed.

## Reference(s):

- [Kalodata-TikTok店铺搜索与详情 API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-kalodata-tiktok-shop)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON files, Shell commands, Configuration guidance]

**Output Format:** [Markdown tables or grouped profiles, with full API responses saved as JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Large responses may be summarized in stdout; full responses are persisted under a local linkfox session data directory, and repeated requests may use a 24-hour local cache.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
