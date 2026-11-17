## Description:

Reverse-looks up Ozon search keywords for up to 20 SKU IDs using Seerfar data, returning organic and ad term metrics for listing optimization and competitor traffic analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce operators and agents use this skill to query Seerfar for Ozon SKU reverse keyword data, compare organic and ad traffic terms, and prepare market-metric tables for listing optimization and competitor analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires LinkFox account or API credentials.

Mitigation: Install only when the publisher and destination service are trusted, store API keys as secrets, and avoid exposing credentials in prompts, logs, or shared output.

Risk: The onboarding flow can create paid orders when billing help is requested.

Mitigation: Require explicit user confirmation before selecting a plan or payment method, and present order details before any payment step.

Risk: Lookup responses and session metadata are persisted locally.

Mitigation: Review saved files before sharing a workspace and delete cached or session data when SKU, market, or account information should not persist.

Risk: Endpoint override environment variables can redirect requests.

Mitigation: Use default LinkFox endpoints unless the alternative gateway is fully trusted and intentionally configured.

Risk: Automatic feedback reporting may disclose task context or result-quality signals to the publisher.

Mitigation: Review or disable feedback reporting behavior before deployment in sensitive workflows.

## Reference(s):

- [Seerfar Ozon keyword back-search API reference](references/api.md)
- [Authentication and billing onboarding](references/onboarding.md)
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-seerfar-ozon-keyword-back-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance, JSON API responses, and saved JSON data files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full lookup responses are saved locally; small responses can be printed inline, while large responses are summarized with pointers to the saved JSON file.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
