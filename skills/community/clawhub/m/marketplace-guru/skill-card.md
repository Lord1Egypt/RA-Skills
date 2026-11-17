## Description:

Marketplace Guru helps users find and compare products on marketplaces by forcing disciplined purchase intent, clean search briefs, multi-source market mapping, price/risk analysis, and decision-ready recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pe4atnik](https://clawhub.ai/user/pe4atnik)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to compare marketplace products, prices, delivery options, sellers, and risks before deciding what to buy. It is intended for region-aware shopping research, exact-item verification, and alternative recommendations without completing purchases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The advertised read-only boundary is weakened because high-impact shopping or account actions may occur after confirmation.

Mitigation: Review deployment policy before use and require explicit human confirmation for checkout, cart, login, payment, account settings, form submissions, and seller messaging, or restrict the skill to read-only browsing.

Risk: Marketplace browsing may use a logged-in browser profile, which can expose account-specific prices, delivery slots, discounts, and session context.

Mitigation: Use an isolated browser profile with no saved payment details for shopping research and avoid granting unnecessary account access.

Risk: Marketplace pages can be blocked, stale, or incomplete, which may make price, delivery, seller, or stock data unreliable.

Mitigation: Require the skill to state searched sources, filters, blockers, and unverified fields before a recommendation is used.

## Reference(s):

- [Marketplace Guru on ClawHub](https://clawhub.ai/pe4atnik/skills/marketplace-guru)
- [Marketplace Guru design notes](artifact/references/design-notes.md)
- [Legacy references](artifact/references/legacy/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown recommendations with search audits, market maps, product comparisons, prices, delivery notes, links, and risk labels]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include unverified-item notes and source blockers when marketplace data cannot be confirmed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
