## Description:

Searches and filters TikTok Shop product data from FastMoss across 15 markets, including keyword and category filters, sales and GMV metrics, commission rates, creator counts, and shop attributes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Sellers, marketers, and agents use this skill to retrieve TikTok Shop product-search results and present comparable product metrics such as sales, GMV, commission rate, price, rating, creator count, and shop flags. It is for product data lookup and comparison, not subjective product-listing or business advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill sends TikTok product-search parameters and selected session metadata to LinkFox/FastMoss.

Mitigation: Use only with data suitable for those services, and do not override service endpoints unless the destination is trusted.

Risk: The security review says the skill handles API keys, login, account credits, payment flows, and feedback submission.

Mitigation: Avoid exposing long-lived API keys in shell history or shared profile files, and require explicit approval before feedback submission or payment orders.

Risk: The skill stores complete API responses on disk and may also cache responses.

Mitigation: Review saved response files before sharing or committing them, and delete stale session or cache data when it is no longer needed.

## Reference(s):

- [FastMoss-TikTok商品搜索 API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-fastmoss-product-search)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown tables or JSON summaries, with full JSON responses saved to local files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Caches identical requests for 24 hours; page size is capped at 10; full responses may be written under LinkFox session data.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
