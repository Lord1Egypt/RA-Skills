## Description:

Golgent Lifestyle Discovery helps AI agents turn everyday user intent into actionable lifestyle recommendations across shopping, dining, local services, travel, and everyday decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uoryon](https://clawhub.ai/user/uoryon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to turn shopping, dining, food delivery, local service, travel, and everyday choice requests into structured recommendation queries and concise option summaries. It is most useful when users need personalized recommendations, nearby options, price or platform filters, or help comparing lifestyle choices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recommendation queries are sent to an external API and may include user intent, filters, and location-related context.

Mitigation: Use the skill only when the user is comfortable sending the query to ads-api.usekairos.ai; never transmit phone numbers, email addresses, real names, IDs, payment data, passwords, or tokens.

Risk: Optional profile fields and precise location can be sensitive.

Mitigation: Require explicit consent before sending profile data, omit profile fields when consent is declined, and request precise location only for food delivery scenarios that need it.

Risk: Automatic impression URL fetching can contact tracking endpoints.

Mitigation: Avoid automatic impression fetching unless the destination domains are reviewed and constrained to approved domains.

Risk: The artifact describes local services and travel discovery, while the positioning evidence marks local services, travel, and activities as planned categories.

Mitigation: Treat local-services and travel recommendations as limited or emerging unless current API behavior is verified before release.

## Reference(s):

- [API Reference](references/api.md)
- [Examples & Templates](references/examples.md)
- [Positioning & Use-Case Mapping](references/positioning.md)
- [Privacy & Data Policy](references/privacy.md)
- [Recommendation API Endpoint](https://ads-api.usekairos.ai/ads/neo)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown guidance with JSON request payloads, shell examples, code examples, and recommendation result tables.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces concise actionable options; API-backed results should include transparency notes and CTA links.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
