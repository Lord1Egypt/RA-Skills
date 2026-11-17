## Description:

Retrieves detailed Walmart product information through WallySmarter, including current attributes, price history, and sales trend data for a single Walmart ItemId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and e-commerce operators use this skill to look up a specific Walmart product by ItemId and review product attributes, price history, stock signals, fulfillment details, and sales estimates. It is intended for single-product analysis, not keyword search, bulk comparison, or seller account reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires LinkFox credentials and may involve phone/SMS onboarding data.

Mitigation: Install only in environments where sharing LinkFox credentials and onboarding data is acceptable, and prefer pre-provisioned credentials over ad hoc registration.

Risk: Full product-query responses and query history may be stored locally.

Mitigation: Review local response storage and cache locations before use, and remove saved data when it is no longer needed.

Risk: Feedback may be submitted externally without clear user consent.

Mitigation: Review or disable automatic feedback submission before deployment, especially in workflows involving sensitive user intent or product research.

Risk: The onboarding flow can initiate billing and order actions.

Mitigation: Require explicit user confirmation before listing paid plans, creating orders, or displaying payment details.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-wallysmarter-product-detail)
- [WallySmarter API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API results, concise summaries, and shell command examples when onboarding is required]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full product-detail responses may be saved locally; large responses are summarized unless inline output is requested.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
