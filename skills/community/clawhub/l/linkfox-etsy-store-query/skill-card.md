## Description:

按多维度筛选 Etsy 店铺（销量、收藏、评论、开店时间、国家、主营类目、Raving/星标等）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce operators, sellers, and analysts use this skill to query Etsy stores and filter them by sales, weekly sales, favorites, reviews, opening date, country, category, Raving status, and star status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill interacts with LinkFox account, API key, billing, and payment-order flows.

Mitigation: Use the official LinkFox site for login and key management when possible, review payment details before creating orders, and install only if those account and billing interactions are acceptable.

Risk: Credentials, OTPs, or API keys may be exposed through command history or shared shell profiles.

Mitigation: Avoid passing OTPs in reusable shell history, store API keys only in trusted local profiles or secret managers, and restart sessions after credential changes.

Risk: Endpoint override environment variables can redirect requests away from the default LinkFox services.

Mitigation: Set LinkFox endpoint override variables only when the destination is trusted and intentionally configured.

Risk: Store queries consume LinkFox credits based on returned store count and can incur larger-than-expected usage.

Mitigation: Warn users before broad queries, start with narrow filters and smaller page sizes, and continue only after the user accepts the credit cost.

## Reference(s):

- [_ehunt_storeQuery API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-etsy-store-query)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration instructions, Guidance, Files]

**Output Format:** [Markdown guidance with JSON command output and saved JSON response files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full query responses are saved under a linkfox session data directory; large responses are summarized unless inline output is requested.]

## Skill Version(s):

1.0.10 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
