## Description:

Queries and filters Temu store records by store identity, country site, category, fulfillment model, sales, revenue, rating, reviews, followers, product count, and listing date.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and ecommerce analysts use this skill to find, rank, and compare Temu stores across operational and sales-performance filters. Agents can also guide users through LinkFox API-key setup and billing recovery when authentication or balance errors block a query.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles LinkFox API keys, SMS-code login, and payment-order flows.

Mitigation: Use LinkFox's official site or an OS credential manager for credentials, avoid entering SMS codes or API keys in logged terminals, and review onboarding prompts before continuing.

Risk: Custom LINKFOX_* endpoint variables could redirect API-key-bearing requests to an untrusted service.

Mitigation: Use the default LinkFox endpoints unless the custom endpoint is fully trusted and expected for the deployment.

Risk: Queries consume LinkFox credits dynamically based on the returned store count, and additional pages trigger additional billed requests.

Mitigation: Use narrow filters and small page sizes first, show expected billing implications when available, and ask the user before running broad or repeated page queries.

Risk: The query script saves full API responses as local JSON files, which may retain business search results beyond the chat response.

Mitigation: Store outputs only in appropriate workspaces and remove saved response files when they are no longer needed.

## Reference(s):

- [Temu Store Query API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-temu-store-query)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, files, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell commands, and JSON query results or summaries; full API responses may be written to JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a LinkFox API key; pageSize is capped at 100; identical query responses may be cached for 24 hours; large responses are summarized while full responses are saved.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
