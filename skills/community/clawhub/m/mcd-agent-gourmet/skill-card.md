## Description:

Helps compare complete McDonald’s China meals by budget and preferences, check coupons and points, and verify current prices without placing orders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[polaris-smart](https://clawhub.ai/user/polaris-smart)

### License/Terms of Use:

MIT-0

## Use Case:

Customers and their assistants use this skill to compare meals for a chosen McDonald’s China store and ordering channel, check coupon time windows and eligibility, and review points before deciding what to buy. It provides read-only guidance; purchases happen through official channels.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: A local account token or raw coupon and delivery-address details could expose private information.

Mitigation: Keep the token in private local configuration, avoid sharing raw account or address details, and disclose only the minimum needed for the user’s decision.

Risk: Saved snapshots or mismatched stores and ordering channels could produce stale prices or misleading coupon claims.

Mitigation: Treat snapshots as demonstrations and use current, store- and channel-specific checks before reporting prices or confirmed discounts.

Risk: Estimated nutrition totals and unverified coupon conditions could be mistaken for guarantees.

Mitigation: Label unknown or unverified details, retain official coupon conditions, and avoid presenting meal comparisons as medical advice.

## Reference(s):

- [McDonald’s China MCP integration](https://github.com/M-China/mcd-mcp-server)
- [MCP capabilities and supported scope](references/mcp-capabilities.md)
- [Validation and limitations](references/validation.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Conversational recommendations and meal comparison tables; optional structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prices and coupon applicability require current store- and channel-specific verification; demonstration snapshots are not current offers.]

## Skill Version(s):

0.3.2 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
