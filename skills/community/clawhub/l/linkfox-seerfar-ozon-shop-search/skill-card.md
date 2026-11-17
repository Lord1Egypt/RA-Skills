## Description:

Looks up the product catalog for a specific Ozon shop or seller from Seerfar data, including 30-day sales, price, rating, weight, fulfillment model, seller type, return/cancellation rate, and shop-level sales context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze one Ozon shop's product catalog, best sellers, seller type, fulfillment split, pricing, and 30-day sales metrics for competitor-shop analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles LinkFox API keys and can guide phone/SMS login.

Mitigation: Use it only in a trusted workspace, avoid sharing credentials in prompts or logs, and rotate any API key that appears in shell history, files, or conversation output.

Risk: The onboarding flow can create payment orders and the shop lookup consumes paid compute credits.

Mitigation: Confirm the user's intent before billing actions or repeated lookups, rely on the 24-hour cache for identical parameters, and explain additional cost before pagination or retries.

Risk: Full API responses are stored locally and may include business-sensitive shop or product analysis data.

Mitigation: Run in an appropriate project workspace, review saved files under the generated linkfox data directory, and delete retained JSON responses when they are no longer needed.

Risk: Endpoint override environment variables can redirect API, login, or billing requests.

Mitigation: Avoid setting LinkFox endpoint override variables unless the destination is trusted and expected for the current environment.

Risk: The skill may send feedback to LinkFox without a separate confirmation when it detects quality or outcome signals.

Mitigation: Review this behavior before installation and avoid including sensitive user or business details in feedback content.

## Reference(s):

- [Seerfar Ozon Shop Search API Reference](artifact/references/api.md)
- [Authentication and Billing Onboarding](artifact/references/onboarding.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API results, shell commands, configuration snippets, and saved JSON response files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full API responses are written to local JSON files; small responses may also be printed inline, while larger responses are summarized unless inline output is requested.]

## Skill Version(s):

1.0.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
