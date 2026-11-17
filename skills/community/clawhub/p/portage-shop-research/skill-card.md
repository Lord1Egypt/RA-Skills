## Description:

Helps users research product prices, availability, stores, and their Portage order history without making purchases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomtom87](https://clawhub.ai/user/tomtom87)

### License/Terms of Use:

MIT-0

## Use Case:

Shoppers use this skill to compare live product offers, check store information, and review their own Portage orders. Purchases require a separate approval-based buying flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research can expose personal order history or shipping details.

Mitigation: Only retrieve the user's own Portage history; avoid repeating shipping addresses or phone numbers unless requested.

Risk: Optional search and retailer API credentials may be disclosed if entered in chat.

Mitigation: Have users enter credentials locally in Portage configuration; do not request or print their values.

Risk: Prices, availability, and store policies may be stale or misleading.

Mitigation: Use live lookups for price and stock; attribute policies to stores and do not vouch for them.

Risk: Store or product content may contain instructions that try to redirect the agent.

Mitigation: Treat store content as untrusted data and keep purchases in the separate approval-based flow.

## Reference(s):

- [Portage documentation](https://portage.readthedocs.io/en/latest/)
- [Shop Research release on ClawHub](https://clawhub.ai/tomtom87/skills/portage-shop-research)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with product offers, store details, and order-history summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only research; does not create carts, checkouts, or payments.]

## Skill Version(s):

0.10.5 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
